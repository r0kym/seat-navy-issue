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

import sni.conf as conf


def main():
    """
    Entry point.
    """

    # --------------------------------------------------------------------------
    # Parsing command line arguments and loading configuration file
    # --------------------------------------------------------------------------
    arguments = parse_command_line_arguments()
    try:
        conf.load_configuration_file(arguments.file)
    except RuntimeError as error:
        logging.fatal(str(error))
        sys.exit(-1)
    logging.config.dictConfig(conf.get('logging', {}))

    # --------------------------------------------------------------------------
    # Pre database init actions
    # --------------------------------------------------------------------------

    if arguments.print_openapi_spec:
        import sni.apiserver as apiserver
        apiserver.print_openapi_spec()
        sys.exit()

    # --------------------------------------------------------------------------
    # Post database init actions, pre database migration
    # --------------------------------------------------------------------------

    import sni.db as db

    if arguments.reload_esi_openapi_spec:
        import sni.esi.esi as esi
        esi.load_esi_openapi()
        sys.exit()

    # --------------------------------------------------------------------------
    # Post database migration, pre scheduler init
    # --------------------------------------------------------------------------

    db.migrate()

    if arguments.migrate_database:
        sys.exit()

    if arguments.run_job:
        module_name, function_name = arguments.run_job.split(':')
        logging.info('Manually running job %s (%s)', function_name,
                     module_name)
        module = __import__(module_name, fromlist=[None])
        function = getattr(module, function_name)
        function()
        sys.exit()

    # --------------------------------------------------------------------------
    # Scheduler init, and start
    # --------------------------------------------------------------------------

    from sni.scheduler import scheduler

    scheduler.start()

    import sni.esi.jobs

    if conf.get('teamspeak.enabled'):
        import sni.teamspeak.jobs

    # --------------------------------------------------------------------------
    # API server start
    # --------------------------------------------------------------------------

    import sni.apiserver as apiserver
    apiserver.start()

    # --------------------------------------------------------------------------
    # API server stopped, cleanup time
    # --------------------------------------------------------------------------

    scheduler.shutdown()


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


if __name__ == '__main__':
    main()
