"""
Configuration facility
"""

from enum import Enum
import logging
from pathlib import Path
from typing import Union
from ipaddress import IPv4Address, IPv6Address

import pydantic as pdt
from pydantic_loader.yaml_config import load_yaml

IPAddress = Union[IPv4Address, IPv6Address]

# class PortNumber(int):
#     """
#     A pydantic-compatible port number
#     """

#     @classmethod
#     def __get_validators__(cls):
#         """
#         See `pydantic Custom Data Types <https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types>`_
#         """
#         yield cls.validate

#     @classmethod
#     def __modify_schema__(cls, field_schema: dict) -> None:
#         """
#         See `pydantic Custom Data Types <https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types>`_
#         """
#         field_schema.update(
#             title='Port number',
#             examples=['80', '9000'],
#         )

#     @classmethod
#     def validate(cls, value: Any) -> 'PortNumber':
#         """
#         Validates the value. yep
#         """
#         if not isinstance(value, (int, str)):
#             raise TypeError('int or str required')
#         value = int(value)
#         if not 0 <= value <= 65535:
#             raise ValueError('Invalid port number (must be between 0 and 65535)')
#         return PortNumber(value)


class DatabaseConfig(pdt.BaseModel):
    """
    Database configuration model
    """
    authentication_source: str = 'admin'
    database: str = 'sni'
    host: str
    password: pdt.SecretStr
    port: int = 27017
    username: str = 'sni'


class DiscordConfig(pdt.BaseModel):
    """
    Discord configuration model
    """
    auth_channel_id: int = -1
    enabled: bool = False
    log_channel_id: int = -1
    server_id: int = -1
    token: pdt.SecretStr = pdt.SecretStr('')


class ESIConfig(pdt.BaseModel):
    """
    ESI configuration model
    """
    client_id: pdt.SecretStr
    client_secret: pdt.SecretStr


class GeneralConfig(pdt.BaseModel):
    """
    General configuration model
    """
    class LoggingLevel(str, Enum):
        """
        Acceptable logging levels
        """
        CRITICAL = 'critical'
        DEBUG = 'debug'
        ERROR = 'error'
        INFO = 'info'
        WARNING = 'warning'

    debug: bool = False
    host: IPAddress = IPv4Address('0.0.0.0')
    logging_level: LoggingLevel = LoggingLevel.INFO
    port: int = 80
    root_url: pdt.HttpUrl
    scheduler_thread_count: int = 5

    @property
    def logging_level_int(self) -> int:
        """
        Returns the int equivalent of the ``logging_level`` field.
        """
        return {
            GeneralConfig.LoggingLevel.CRITICAL: logging.CRITICAL,
            GeneralConfig.LoggingLevel.DEBUG: logging.DEBUG,
            GeneralConfig.LoggingLevel.ERROR: logging.ERROR,
            GeneralConfig.LoggingLevel.INFO: logging.INFO,
            GeneralConfig.LoggingLevel.WARNING: logging.WARNING,
        }[self.logging_level]


class JWTConfig(pdt.BaseModel):
    """
    JWT configuration model
    """
    class JWTAlgorithm(str, Enum):
        """
        Acceptable JWT algorithms, see `here <https://pyjwt.readthedocs.io/en/latest/algorithms.html?highlight=algorithm#digital-signature-algorithms>`_.
        """
        # ES256 = 'ES256'
        # ES384 = 'ES384'
        # ES512 = 'ES512'
        HS256 = 'HS256'
        HS384 = 'HS384'
        HS512 = 'HS512'
        # PS256 = 'PS256'
        # PS384 = 'PS384'
        # PS512 = 'PS512'
        # RS256 = 'RS256'
        # RS384 = 'RS384'
        # RS512 = 'RS512'

    algorithm: JWTAlgorithm = JWTAlgorithm.HS256
    secret: pdt.SecretBytes


class RedisConfig(pdt.BaseModel):
    """
    Redis configuration model
    """
    database: int = 0
    host: str
    port: int = 6379


class TeamspeakConfig(pdt.BaseModel):
    """
    Teamspeak configuration model
    """
    auth_group_name: str = 'SNI TS AUTH'
    bot_name: str = 'SeAT Navy Issue'
    enabled: bool = False
    host: IPAddress = IPv4Address('0.0.0.0')
    password: pdt.SecretStr = pdt.SecretStr('')
    port: int = 10011
    server_id: int = 0
    username: str = 'sni'


class Config(pdt.BaseSettings):
    """
    SNI configuration model
    """
    database: DatabaseConfig
    discord: DiscordConfig
    esi: ESIConfig
    general: GeneralConfig
    jwt: JWTConfig
    redis: RedisConfig
    teamspeak: TeamspeakConfig


CONFIGURATION: Config


def load_configuration_file(path: str) -> None:
    """
    Loads the configuration from a YAML file.
    """
    global CONFIGURATION
    CONFIGURATION = load_yaml(Config, Path(path))
