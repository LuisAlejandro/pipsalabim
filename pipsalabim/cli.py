# -*- coding: utf-8 -*-
#
#   This file is part of Pip Sala Bim.
#   Copyright (C) 2016, Pip Sala Bim Developers.
#
#   Please refer to AUTHORS.rst for a complete list of Copyright holders.
#
#   Pip Sala Bim is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Pip Sala Bim is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses.
"""
``pipsalabim.cli`` is a module for handling the command line interface.

This module handles the commands for using Pip Sala Bim. It also parses
parameters, show help, version and controls the logging level.
"""
from __future__ import absolute_import, print_function

from argparse import ArgumentParser

from . import __version__, __description__
from .core.logger import logger
from .api.report import main as report
from .api.update import main as update


def commandline(argv=None):
    """
    Configure ``ArgumentParser`` to accept custom arguments and commands.

    :param argv: a list of commandline arguments like ``sys.argv``.
                 For example::

                    ['-v', '--loglevel', 'INFO']

    :return: a ``Namespace`` object.

    .. versionadded:: 0.1.0
    """
    assert isinstance(argv, (list, type(None)))

    parser = ArgumentParser(description=__description__)
    parser.add_argument(
        '-V', '--version', action='version',
        version='pipsalabim {0}'.format(__version__),
        help='Print version and exit.')
    parser.add_argument(
        '-l', '--loglevel', default='WARNING', metavar='<level>',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        help='Logger verbosity level (default: WARNING).')

    subparsers = parser.add_subparsers(title='commands')
    report_parser = subparsers.add_parser('report')
    report_parser.set_defaults(command=report)
    report_parser.add_argument(
        '-r', '--requirements', action='store_true',
        help='Format output for requirements.txt file.')

    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(command=update)

    return parser.parse_args(argv)


def main(argv=None):
    """
    Handle arguments and commands.

    :param argv: a list of commandline arguments like ``sys.argv``.
                 For example::

                    ['-v', '--loglevel', 'INFO']

    :return: an exit status.

    .. versionadded:: 0.1.0
    """
    assert isinstance(argv, (list, type(None)))

    args = commandline(argv)

    logger.start()
    logger.loglevel(args.loglevel)
    logger.info('Starting execution.')

    try:
        status = args.command(**vars(args))
    except KeyboardInterrupt:
        logger.critical('Execution interrupted by user!')
        status = 1
    except Exception as e:
        logger.exception(e)
        logger.critical('Shutting down due to fatal error!')
        status = 1
    else:
        logger.info('Ending execution.')

    logger.stop()
    return status


if __name__ == '__main__':
    import re
    import sys
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
