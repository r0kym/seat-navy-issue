# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import
"""
Main module

This module contains the entry point to SNI.
"""

from importlib import import_module
import argparse
import logging
import logging.config
import sys

from pydantic_loader.config import CfgError

from sni.utils import object_from_name
from sni.conf import load_configuration_file


def connect_database_signals() -> None:
    """
    Imports all ``signals`` submodules.
    """
    from sni.conf import CONFIGURATION as conf

    modules = {
        "sni.db.signals": True,
        "sni.esi.signals": True,
        "sni.sde.signals": True,
        "sni.index.signals": True,
        "sni.uac.signals": True,
        "sni.user.signals": True,
        "sni.api.signals": True,
        "sni.discord.signals": conf.discord.enabled,
        "sni.teamspeak.signals": conf.teamspeak.enabled,
    }
    logging.debug("Connecting database signals")
    for module, include in modules.items():
        if include:
            import_module(module)


def configure_logging() -> None:
    """
    Basic configuration of the logging facility
    """
    from sni.conf import CONFIGURATION as conf

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": conf.general.logging_level_int,
                },
                # 'discord': {
                #     'handlers': ['default'],
                #     'level': logging.WARNING,
                # },
                # 'websockets': {
                #     'handlers': ['default'],
                #     'level': logging.WARNING,
                # },
            },
        }
    )


def migrate_database() -> None:
    """
    Inits and migrate the MongoDB database.
    """
    from sni.conf import CONFIGURATION as conf

    migrations = {
        "sni.esi.migration:migrate": True,
        "sni.sde.migration:migrate": True,
        "sni.index.migration:migrate": True,
        "sni.uac.migration:migrate": True,
        "sni.user.migration:migrate": True,
        "sni.api.migration:migrate": True,
        "sni.discord.migration:migrate": conf.discord.enabled,
        "sni.teamspeak.migration:migrate": conf.teamspeak.enabled,
    }
    logging.debug("Running migration jobs")
    for function, include in migrations.items():
        if include:
            object_from_name(function)()


def main():
    """
    Entry point.
    """

    # --------------------------------------------------------------------------
    # Parsing command line arguments and loading configuration file
    # --------------------------------------------------------------------------

    arguments = parse_command_line_arguments()

    if arguments.print_configuration_spec:
        from sni.conf import print_configuration_schema

        print_configuration_schema()
        sys.exit()

    try:
        load_configuration_file(arguments.file)
    except CfgError:
        print("Error loading configuration file " + arguments.file)
        sys.exit(-1)
    from sni.conf import CONFIGURATION as conf

    configure_logging()

    # --------------------------------------------------------------------------
    # Pre database
    # --------------------------------------------------------------------------

    if arguments.print_openapi_spec:
        from sni.api.server import print_openapi_spec

        print_openapi_spec()
        sys.exit()

    if arguments.flush_cache:
        from sni.db.cache import new_redis_connection

        logging.info("Flushing Redis cache")
        new_redis_connection().flushdb()

    # --------------------------------------------------------------------------
    # Database migration
    # --------------------------------------------------------------------------

    from sni.db.mongodb import init_mongodb

    init_mongodb()
    migrate_database()

    if arguments.migrate_database:
        sys.exit()

    connect_database_signals()

    # --------------------------------------------------------------------------
    # Post database migration, pre sheduler start
    # --------------------------------------------------------------------------

    from sni.esi.esi import load_esi_openapi

    load_esi_openapi()
    if arguments.reload_esi_openapi_spec:
        sys.exit()

    # --------------------------------------------------------------------------
    # Scheduler start
    # --------------------------------------------------------------------------

    from sni.scheduler import start_scheduler, stop_scheduler

    start_scheduler()
    schedule_jobs()

    # --------------------------------------------------------------------------
    # Pre API server start
    # --------------------------------------------------------------------------

    if conf.discord.enabled:
        start_discord_bot()

    # --------------------------------------------------------------------------
    # API server start
    # --------------------------------------------------------------------------

    from sni.api.server import start_api_server
    import sni.api.exception_handlers

    start_api_server()

    # --------------------------------------------------------------------------
    # API server stopped, cleanup time
    # --------------------------------------------------------------------------

    stop_scheduler()


def parse_command_line_arguments() -> argparse.Namespace:
    """Parses command line arguments

    See also:
        `argparse documentation
        <https://docs.python.org/3/library/argparse.html>`_
    """
    argument_parser = argparse.ArgumentParser(description="SeAT Navy Issue")
    argument_parser.add_argument(
        "-f",
        "--file",
        action="store",
        default="./sni.yml",
        help="Specify an alternate configuration file (default: ./sni.yml)",
    )
    argument_parser.add_argument(
        "--flush-cache",
        action="store_true",
        default=False,
        help="Flushes the Redis cache",
    )
    argument_parser.add_argument(
        "--migrate-database",
        action="store_true",
        default=False,
        help="Runs database migration jobs and exits",
    )
    argument_parser.add_argument(
        "--print-configuration-spec",
        action="store_true",
        default=False,
        help="Prints the configuration file specification in JSON and exits",
    )
    argument_parser.add_argument(
        "--print-openapi-spec",
        action="store_true",
        default=False,
        help="Prints the OpenAPI specification in YAML and exits",
    )
    argument_parser.add_argument(
        "--reload-esi-openapi-spec",
        action="store_true",
        default=False,
        help="Reloads the ESI OpenAPI specification to the database and exits",
    )
    return argument_parser.parse_args()


def start_discord_bot() -> None:
    """
    Starts the discord bot (or rather, schedules it to be started), and
    corrects the Discord command and event handlers.
    """
    from sni.scheduler import scheduler
    from sni.discord.bot import start_bot
    import sni.discord.commands
    import sni.discord.events

    scheduler.add_job(start_bot)


def schedule_jobs() -> None:
    """
    Schedules jobs from all subpackages
    """
    from sni.conf import CONFIGURATION as conf

    modules = {
        "sni.db.jobs": True,
        "sni.esi.jobs": True,
        "sni.sde.jobs": True,
        "sni.uac.jobs": True,
        "sni.user.jobs": True,
        "sni.index.jobs": True,
        "sni.api.jobs": True,
        "sni.discord.jobs": conf.discord.enabled,
        "sni.teamspeak.jobs": conf.teamspeak.enabled,
    }
    logging.debug("Scheduling jobs")
    for module, include in modules.items():
        if include:
            import_module(module)


if __name__ == "__main__":
    main()
