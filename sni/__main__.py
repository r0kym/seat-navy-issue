"""
Main module

This module contains the entry point to SNI.
"""

import argparse
import logging
import logging.config
import pprint
import sys
import uvicorn
import yaml

import sni.apiserver as apiserver
import sni.conf as conf
import sni.db as db
import sni.esi as esi


def main():
    """
    Entry point.
    """
    arguments = parse_command_line_arguments()

    try:
        conf.load_configuration_file(arguments.file)
    except RuntimeError as error:
        logging.fatal(str(error))
        sys.exit(-1)
    logging.config.dictConfig(conf.get('logging', {}))

    if arguments.migrate_database:
        db.init()
        db.migrate()
        sys.exit()
    if arguments.print_openapi_spec:
        apiserver.print_openapi_spec()
        sys.exit()
    if arguments.reload_esi_openapi_spec:
        db.init()
        esi.load_esi_openapi()
        sys.exit()

    if conf.get('general.debug'):
        logging.debug('SNI running in debug mode, dumping configuration:')
        pprint.pprint(conf.CONFIGURATION, depth=1)

    db.init()
    db.migrate()
    start_api_server()


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


def start_api_server() -> None:
    """
    Runs the API server.
    """
    logging.info('Starting API server on %s:%s', conf.get('general.host'),
                 conf.get('general.port'))
    uvicorn.run(
        'sni.apiserver:app',
        host=conf.get('general.host'),
        log_level='debug' if conf.get('general.debug') else 'info',
        port=conf.get('general.port'),
    )


if __name__ == '__main__':
    main()
