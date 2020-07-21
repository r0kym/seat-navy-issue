# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import
"""
Main module

This module contains the entry point to SNI.
"""

from importlib import import_module
import argparse
import asyncio
from inspect import iscoroutinefunction
import logging
import sys

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
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        level=logging_level,
    )
    logging.getLogger('apscheduler').setLevel(logging_level)
    logging.getLogger('discord').setLevel(logging_level)
    logging.getLogger('fastapi').setLevel(logging_level)
    logging.getLogger('uvicorn').setLevel(logging_level)


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
        import sni.api.server
        sni.api.server.print_openapi_spec()
        sys.exit()

    # --------------------------------------------------------------------------
    # Database migration
    # --------------------------------------------------------------------------

    import sni.db.mongodb
    sni.db.mongodb.init()
    connect_database_signals()
    migrate_database()

    if arguments.migrate_database:
        sys.exit()

    # --------------------------------------------------------------------------
    # Post database migration, pre sheduler start
    # --------------------------------------------------------------------------

    if arguments.reload_esi_openapi_spec:
        import sni.esi.esi
        sni.esi.esi.load_esi_openapi()
        sys.exit()

    import sni.scheduler

    if arguments.run_job:
        run_job(arguments.run_job)
        sys.exit()

    # --------------------------------------------------------------------------
    # Scheduler start
    # --------------------------------------------------------------------------

    sni.scheduler.start_scheduler()
    schedule_jobs()

    # --------------------------------------------------------------------------
    # Pre API server start
    # --------------------------------------------------------------------------

    if conf.get('discord.enabled'):
        import sni.discord.bot
        import sni.discord.commands
        import sni.discord.events
        sni.discord.bot.start()

    # --------------------------------------------------------------------------
    # API server start
    # --------------------------------------------------------------------------

    import sni.api.server
    import sni.api.exception_handlers
    sni.api.server.start()

    # --------------------------------------------------------------------------
    # API server stopped, cleanup time
    # --------------------------------------------------------------------------

    sni.scheduler.scheduler.shutdown()


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
    argument_parser.add_argument(
        '--run-job',
        help='Runs a job and exists',
    )
    return argument_parser.parse_args()


def run_job(job_name: str) -> None:
    """
    Runs a job (or indeed, any function that doesn't take arguments)
    """
    module_name, function_name = job_name.split(':')
    logging.info('Manually running job %s (%s)', function_name, module_name)
    module = import_module(module_name)
    function = getattr(module, function_name)

    if iscoroutinefunction(function):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(function())
    else:
        import sni.scheduler
        sni.scheduler.ENABLED = False
        function()


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
