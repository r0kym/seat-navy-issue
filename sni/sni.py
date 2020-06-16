"""
Main module

This module contains the entry point to SNI.
"""

import argparse
import logging.config
import uvicorn

import conf


def main():
    """
    Entry point.
    """
    arguments = parse_command_line_arguments()
    conf.load_configuration_file(arguments.file)
    logging.config.dictConfig(conf.get('logging', {}))
    uvicorn.run(
        'apiserver:app',
        host=conf.get('general.host'),
        log_level='debug' if conf.get('general.debug') else 'info',
        port=conf.get('general.port'),
    )


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
    return argument_parser.parse_args()


if __name__ == '__main__':
    main()
