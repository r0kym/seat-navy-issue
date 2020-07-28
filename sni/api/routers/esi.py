"""
ESI related paths
"""

from datetime import datetime
from typing import Callable, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)
import pydantic as pdt

from sni.user.models import User

from sni.esi.token import get_access_token
from sni.esi.esi import (
    esi_get_all_pages,
    esi_get,
    EsiResponse,
    get_esi_path_scope,
    id_annotations,
    id_to_name,
)
from sni.index.models import (
    EsiCharacterLocation,
    EsiMail,
    EsiMailRecipient,
)
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

from .common import paginate

router = APIRouter()


class EsiRequestIn(pdt.BaseModel):
    """
    Data to be forwarded to the ESI
    """
    all_pages: bool = False
    id_annotations: bool = False
    on_behalf_of: Optional[int] = None
    params: dict = {}


class GetCharacterLocationOut(pdt.BaseModel):
    """
    Describes a character location
    """
    character_id: int
    character_name: str
    online: bool
    ship_name: str
    ship_type_id: int
    ship_type_name: str
    solar_system_id: int
    solar_system_name: str
    station_id: Optional[int] = None
    station_name: Optional[str] = None
    structure_id: Optional[int] = None
    timestamp: datetime

    @staticmethod
    def from_record(
            location: EsiCharacterLocation) -> 'GetCharacterLocationOut':
        """
        Converts a :class:`sni.index.models.EsiCharacterLocation` to a
        :class:`sni.api.routers.esi.GetCharacterLocationOut`
        """
        ship_type_name = id_to_name(location.ship_type_id, 'type_id')
        solar_system_name = id_to_name(location.solar_system_id,
                                       'solar_system_id')
        station_name = id_to_name(
            location.station_id,
            'station_id') if location.station_id is not None else None
        return GetCharacterLocationOut(
            character_id=location.user.character_id,
            character_name=location.user.character_name,
            online=location.online,
            ship_name=location.ship_name,
            ship_type_id=location.ship_type_id,
            ship_type_name=ship_type_name,
            solar_system_id=location.solar_system_id,
            solar_system_name=solar_system_name,
            station_id=location.station_id,
            station_name=station_name,
            structure_id=location.structure_id,
            timestamp=location.timestamp,
        )


class GetMailOut(pdt.BaseModel):
    """
    Represents a user email.
    """
    class MailRecipient(pdt.BaseModel):
        """
        Represents a recipient of the email
        """
        recipient_id: int
        recipient_name: str

        @staticmethod
        def from_record(
                recipient: EsiMailRecipient) -> 'GetMailOut.MailRecipient':
            """
            Converts a :class:`sni.index.models.EsiMailRecipient` to a
            :class:`sni.api.routers.esi.GetMailOut.MailRecipient`
            """
            if recipient.recipient_type == 'mailing_list':
                recipient_name = 'Mailing list ' + str(recipient.recipient_id)
            else:
                recipient_name = id_to_name(
                    recipient.recipient_id,
                    recipient.recipient_type + '_id',
                )
            return GetMailOut.MailRecipient(
                recipient_id=recipient.recipient_id,
                recipient_name=recipient_name,
            )

    body: str
    from_id: int
    from_name: str
    mail_id: int
    recipients: List[MailRecipient]
    subject: str
    timestamp: datetime

    @staticmethod
    def from_record(mail: EsiMail) -> 'GetMailOut':
        """
        Converts a :class:`sni.index.models.EsiMail` to a
        :class:`sni.api.routers.esi.GetMailOut`
        """
        recipients = [
            GetMailOut.MailRecipient.from_record(recipient)
            for recipient in mail.recipients
        ]
        return GetMailOut(
            body=mail.body,
            from_id=mail.from_id,
            from_name=mail.from_name,
            mail_id=mail.mail_id,
            recipients=recipients,
            subject=mail.subject,
            timestamp=mail.timestamp,
        )


class GetMailShortOut(pdt.BaseModel):
    """
    Represents a short description (header) of an email
    """

    from_id: int
    from_name: str
    mail_id: int
    recipients: List[GetMailOut.MailRecipient]
    subject: str
    timestamp: datetime

    @staticmethod
    def from_record(mail: EsiMail) -> 'GetMailShortOut':
        """
        Converts a :class:`sni.index.models.EsiMail` to a
        :class:`sni.api.routers.esi.GetMailShortOut`
        """
        recipients = [
            GetMailOut.MailRecipient.from_record(recipient)
            for recipient in mail.recipients
        ]
        return GetMailShortOut(
            from_id=mail.from_id,
            from_name=id_to_name(mail.from_id, 'character_id'),
            mail_id=mail.mail_id,
            recipients=recipients,
            subject=mail.subject,
            timestamp=mail.timestamp,
        )


@router.get(
    '/history/characters/{character_id}/location',
    response_model=List[GetCharacterLocationOut],
    summary='Get character location history',
)
def get_history_character_location(
        character_id: int,
        response: Response,
        page: pdt.PositiveInt = Header(1),
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Get the location history of a character. Requires having clearance to
    access the ESI scopes ``esi-location.read_location.v1``,
    ``esi-location.read_online.v1``, and ``esi-location.read_ship_type.v1``, of
    the character. The results are sorted by most to least recent, and
    paginated by pages of 50 items. The page count in returned in the
    ``X-Pages`` header.
    """
    usr: User = User.objects(character_id=character_id).get()
    assert_has_clearance(tkn.owner, 'esi-location.read_location.v1', usr)
    assert_has_clearance(tkn.owner, 'esi-location.read_online.v1', usr)
    assert_has_clearance(tkn.owner, 'esi-location.read_ship_type.v1', usr)
    query_set = EsiCharacterLocation.objects(user=usr).order_by('-timestamp')
    return [
        GetCharacterLocationOut.from_record(location)
        for location in paginate(query_set, 50, page, response)
    ]


@router.get(
    '/history/characters/{character_id}/mail',
    response_model=List[GetMailShortOut],
    summary='Get character email history',
)
def get_history_character_mails(
        character_id: int,
        response: Response,
        page: pdt.PositiveInt = Header(1),
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Get the email history of a character. Requires having clearance to access
    the ESI scope ``esi-mail.read_mail.v1`` of the character. The results are
    sorted by most to least recent, and paginated by pages of 50 items. The
    page count in returned in the ``X-Pages`` header.

    Todo:
        Only show email sent by the specified user...
    """
    usr: User = User.objects(character_id=character_id).get()
    assert_has_clearance(tkn.owner, 'esi-mail.read_mail.v1', usr)
    query_set = EsiMail.objects(from_id=character_id).order_by('-timestamp')
    return [
        GetMailShortOut.from_record(mail)
        for mail in paginate(query_set, 50, page, response)
    ]


@router.get(
    '/{esi_path:path}',
    response_model=EsiResponse,
    summary='Proxy path to the ESI',
    tags=['ESI'],
)
async def get_esi(
        esi_path: str,
        data: EsiRequestIn = EsiRequestIn(),
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Forwards a `GET` request to the ESI. The required clearance level depends
    on the user making the request and the user specified on the `on_behalf_of`
    field. See also `EsiRequestIn`.
    """
    esi_token: Optional[str] = None
    if data.on_behalf_of:
        esi_scope = get_esi_path_scope(esi_path)
        if esi_scope is not None:
            target = User.objects.get(character_id=data.on_behalf_of)
            assert_has_clearance(tkn.owner, esi_scope, target)
            try:
                esi_token = get_access_token(
                    data.on_behalf_of,
                    esi_scope,
                ).access_token
            except LookupError:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail='Could not find valid ESI refresh token for ' \
                        + 'character ' + str(data.on_behalf_of),
                )

    function: Callable[..., EsiResponse] = \
        esi_get_all_pages if data.all_pages else esi_get
    result = function(
        esi_path,
        token=esi_token,
        kwargs={'params': data.params},
    )
    if data.id_annotations:
        result.id_annotations = id_annotations(result.data)
    return result
