"""
Main module

This module contains the entry point to SNI.
"""

import argparse
import logging.config
import pprint
import sys
import uvicorn
import yaml

import sni.conf as conf


def main():
    """
    Entry point.
    """
    arguments = parse_command_line_arguments()

    if arguments.openapi_spec:
        print_openapi_spec()
        sys.exit()

    try:
        conf.load_configuration_file(arguments.file)
    except RuntimeError as error:
        logging.fatal(str(error))
        sys.exit(-1)

    logging.config.dictConfig(conf.get('logging', {}))

    if conf.get('general.debug'):
        logging.debug('SNI running in debug mode, dumping configuration:')
        pprint.pprint(conf.CONFIGURATION, depth=1)

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
        '--openapi-spec',
        action='store_true',
        default=False,
        help='Prints the OpenAPI specification in YAML',
    )
    return argument_parser.parse_args()


def print_openapi_spec() -> None:
    """
    Print the OpenAPI specification of the server in YAML.
    """
    from sni.apiserver import app  # pylint: disable=import-outside-toplevel
    print(yaml.dump(app.openapi()))


def start_api_server() -> None:
    """
    Runs the API server.
    """
    uvicorn.run(
        'sni.apiserver:app',
        host=conf.get('general.host'),
        log_level='debug' if conf.get('general.debug') else 'info',
        port=conf.get('general.port'),
    )


if __name__ == '__main__':
    main()
