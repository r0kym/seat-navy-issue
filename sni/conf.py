"""
Configuration facility
"""

from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Optional, Union
import logging

import pydantic as pdt
from pydantic_loader.yaml_config import load_yaml


class DatabaseConfig(pdt.BaseModel):
    """
    Database configuration model
    """
    authentication_source: str = pdt.Field(
        default='admin',
        description='The database in which the user belongs.',
    )

    database: str = pdt.Field(
        default='sni',
        description='Database name.',
    )

    host: str = pdt.Field(
        default='mongo',
        description='Database hostname.',
    )

    password: pdt.SecretStr = pdt.Field(default='', description='Password.')

    port: int = pdt.Field(
        default=27017,
        description='Database port.',
        ge=0,
        le=65535,
    )

    username: str = pdt.Field(
        default='sni',
        description='Username.',
    )


class DiscordConfig(pdt.BaseModel):
    """
    Discord configuration model
    """
    auth_channel_id: int = pdt.Field(
        default=0,
        description=(
            'Authentication channel ID. This is where users will start '
            'authentication challenges. Only required if ``discord.enable`` '
            'is set to ``True``.'),
    )

    enabled: bool = pdt.Field(
        default=False,
        description='Wether to activate the Discord connector.',
    )

    log_channel_id: int = pdt.Field(
        default=0,
        description=(
            'Logging channel ID. This is where the Discorb bot will log '
            'events. Only required if ``discord.enable`` is set to ``True``.'),
    )

    server_id: int = pdt.Field(
        default=0,
        description='Discord server (or guild) ID.',
    )

    token: pdt.SecretStr = pdt.Field(
        default=pdt.SecretStr(''),
        description=(
            'Discord bot token. Only required if ``discord.enable`` is set to '
            '``True``.'),
    )


class ESIConfig(pdt.BaseModel):
    """
    ESI configuration model
    """
    client_id: pdt.SecretStr = pdt.Field(
        default='',
        description='ESI client ID.',
    )

    client_secret: pdt.SecretStr = pdt.Field(
        default='',
        description='ESI client secret.',
    )


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

    debug: bool = pdt.Field(
        default=False,
        description=(
            'Wether SNI should run in debug mode. In this mode, logging is '
            'more verbose, and potentially exposes secrets. Do not use in a '
            'production environment.'),
    )

    host: Union[IPv4Address, IPv6Address] = pdt.Field(
        default=IPv4Address('0.0.0.0'),
        description=
        'IP address at which SNI should listen for incoming connections.',
    )

    logging_level: LoggingLevel = pdt.Field(
        default=LoggingLevel.INFO,
        description='Logging level.',
    )

    port: int = pdt.Field(
        default=80,
        description='Port at which SNI should listen for incoming connections.',
        ge=0,
        le=65535,
    )

    root_url: pdt.HttpUrl = pdt.Field(
        default='https://foo.bar',
        description=(
            'URL at which this SNI instance is located. The ESI callback '
            'should then be ``<root_url>/callback/esi``.'),
    )

    scheduler_thread_count: int = pdt.Field(
        default=5,
        description='Number of threads available to the scheduler.',
        ge=1,
    )

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

        HS256 = 'HS256'
        """HMAC using SHA-256 hash algorithm (default)"""

        HS384 = 'HS384'
        """HMAC using SHA-384 hash algorithm"""

        HS512 = 'HS512'
        """HMAC using SHA-512 hash algorithm"""

        # ES256 = 'ES256'
        # """ECDSA signature algorithm using SHA-256 hash algorithm"""

        # ES384 = 'ES384'
        # """ECDSA signature algorithm using SHA-384 hash algorithm"""

        # ES512 = 'ES512'
        # """ECDSA signature algorithm using SHA-512 hash algorithm"""

        # RS256 = 'RS256'
        # """RSASSA-PKCS1-v1_5 signature algorithm using SHA-256 hash algorithm"""

        # RS384 = 'RS384'
        # """RSASSA-PKCS1-v1_5 signature algorithm using SHA-384 hash algorithm"""

        # RS512 = 'RS512'
        # """RSASSA-PKCS1-v1_5 signature algorithm using SHA-512 hash algorithm"""

        # PS256 = 'PS256'
        # """RSASSA-PSS signature using SHA-256 and MGF1 padding with SHA-256"""

        # PS384 = 'PS384'
        # """RSASSA-PSS signature using SHA-384 and MGF1 padding with SHA-384"""

        # PS512 = 'PS512'
        # """RSASSA-PSS signature using SHA-512 and MGF1 padding with SHA-512"""

    algorithm: JWTAlgorithm = pdt.Field(
        default=JWTAlgorithm.HS256,
        description=(
            'JWT algorithm. For now, only symmetric cryptography algorithms '
            'are supported.'),
    )

    secret: pdt.SecretBytes = pdt.Field(
        default=b'',
        description='JWT secret. Generate one with ``openssl rand -hex 32``.',
    )


class RedisConfig(pdt.BaseModel):
    """
    Redis configuration model
    """
    database: int = pdt.Field(
        default=0,
        description='Redis database to use.',
    )

    host: str = pdt.Field(
        default='redis',
        description='Redis hostname.',
    )

    port: int = pdt.Field(
        default=6379,
        description='Redis port.',
        ge=0,
        le=65535,
    )


class TeamspeakConfig(pdt.BaseModel):
    """
    Teamspeak configuration model
    """
    auth_group_name: str = pdt.Field(
        default='SNI TS AUTH',
        description=(
            'Name of the auth group. Authenticated Teamspeak users are '
            'automatically added to this group. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )

    bot_name: str = pdt.Field(
        default='SeAT Navy Issue',
        description=(
            'Name of the Teamspeak bot. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )

    enabled: bool = pdt.Field(
        default=False,
        description='Wether to activate the Teamspeak connector.')

    host: str = pdt.Field(
        default='',
        description=(
            'Name, hostname, or IP address of the Teamspeak server. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )

    password: pdt.SecretStr = pdt.Field(
        default=pdt.SecretStr(''),
        description=(
            'Query server password. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )

    port: int = pdt.Field(
        default=10011,
        description=(
            'Port of the query server associated to the Teamspeak server. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
        ge=0,
        le=65535,
    )

    server_id: int = pdt.Field(
        default=0,
        description=(
            'Teamspeak server ID. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )

    username: str = pdt.Field(
        default='sni',
        description=(
            'Query server username. '
            'Only required if ``teamspeak.enable`` is set to ``True``.'),
    )


class Config(pdt.BaseSettings):
    """
    SNI configuration model
    """
    database: DatabaseConfig = pdt.Field(
        default=DatabaseConfig(),
        description='Database configuration document.',
    )

    discord: DiscordConfig = pdt.Field(
        default=DiscordConfig(),
        description='Discord configuration document.',
    )

    esi: ESIConfig = pdt.Field(
        default=ESIConfig(),
        description='ESI configuration document.',
    )

    general: GeneralConfig = pdt.Field(
        default=GeneralConfig(),
        description='General configuration document.',
    )

    jwt: JWTConfig = pdt.Field(
        default=JWTConfig(),
        description='JWT configuration document.',
    )

    redis: RedisConfig = pdt.Field(
        default=RedisConfig(),
        description='Redis configuration document.',
    )

    teamspeak: TeamspeakConfig = pdt.Field(
        default=TeamspeakConfig(),
        description='Teamspeak configuration document.',
    )


CONFIGURATION: Config = Config()


def load_configuration_file(path: str) -> None:
    """
    Loads the configuration from a YAML file.
    """
    global CONFIGURATION
    CONFIGURATION = load_yaml(Config, Path(path))


def print_configuration_schema(indentation: Optional[int] = 4) -> None:
    """
    Prints the JSON schema of :class:`sni.conf.Config`
    """
    print(Config.schema_json(indent=indentation))
