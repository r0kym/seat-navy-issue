# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import
"""
Main module

This module contains the entry point to SNI.
"""

import argparse
import logging
import logging.config
import sys

from sni.utils import callable_from_name
import sni.conf as conf


def connect_database_signals() -> None:
    """
    Imports all ``signals`` submodules.
    """
    logging.info('Connecting database signals')
    import sni.db.signals
    import sni.esi.signals
    import sni.sde.signals
    import sni.index.signals
    import sni.uac.signals
    import sni.user.signals
    import sni.api.signals

    if conf.get('discord.enabled'):
        import sni.discord.signals

    if conf.get('teamspeak.enabled'):
        import sni.teamspeak.signals


def configure_logging() -> None:
    """
    Basic configuration of the logging facility
    """
    logging_level = {
        'CRITICAL': logging.CRITICAL,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
    }[str(conf.get('general.logging_level')).upper()]
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            },
        },
        'handlers': {
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': logging_level,
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
    })


def migrate_database() -> None:
    """
    Inits and migrate the MongoDB database.
    """
    logging.info('Migrating database')

    import sni.esi.migration
    sni.esi.migration.migrate()

    import sni.sde.migration
    sni.sde.migration.migrate()

    import sni.index.migration
    sni.index.migration.migrate()

    import sni.uac.migration
    sni.uac.migration.migrate()

    import sni.user.migration
    sni.user.migration.migrate()

    import sni.api.migration
    sni.api.migration.migrate()

    if conf.get('discord.enabled'):
        import sni.discord.migration
        sni.discord.migration.migrate()

    if conf.get('teamspeak.enabled'):
        import sni.teamspeak.migration
        sni.teamspeak.migration.migrate()


def main():
    """
    Entry point.
    """

    # --------------------------------------------------------------------------
    # Parsing command line arguments and loading configuration file
    # --------------------------------------------------------------------------

    arguments = parse_command_line_arguments()
    conf.load_configuration_file(arguments.file)
    configure_logging()

    # --------------------------------------------------------------------------
    # Pre database
    # --------------------------------------------------------------------------

    if arguments.print_openapi_spec:
        from sni.api.server import print_openapi_spec
        print_openapi_spec()
        sys.exit()

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

    if conf.get('discord.enabled'):
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
    argument_parser = argparse.ArgumentParser(description='SeAT Navy Issue')
    argument_parser.add_argument(
        '-f',
        '--file',
        action='store',
        default='./sni.yml',
        help='Specify an alternate configuration file (default: ./sni.yml)',
    )
    argument_parser.add_argument(
        '--migrate-database',
        action='store_true',
        default=False,
        help='Runs database migration jobs and exits',
    )
    argument_parser.add_argument(
        '--print-openapi-spec',
        action='store_true',
        default=False,
        help='Prints the OpenAPI specification in YAML and exits',
    )
    argument_parser.add_argument(
        '--reload-esi-openapi-spec',
        action='store_true',
        default=False,
        help='Reloads the ESI OpenAPI specification to the database and exits',
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
    logging.info('Scheduling jobs')
    import sni.db.jobs
    import sni.esi.jobs
    import sni.sde.jobs
    import sni.uac.jobs
    import sni.user.jobs
    import sni.index.jobs
    import sni.api.jobs

    if conf.get('teamspeak.enabled'):
        import sni.teamspeak.jobs

    if conf.get('discord.enabled'):
        import sni.discord.jobs


if __name__ == '__main__':
    main()
