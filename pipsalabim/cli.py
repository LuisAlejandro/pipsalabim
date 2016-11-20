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

This modue handles the commands for using Pip Sala Bim. It also parses
parameters, show help, version and controls the logging level.
"""
from __future__ import absolute_import

from argparse import ArgumentParser

from . import __version__, __description__
from .core.logger import logger
from .api.report import main as report
from .api.update import main as update


def main(argv=None):
    """
    Handle arguments and commands.

    :return: exit status.

    .. versionadded:: 0.1.0
    """
    parser = ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', action='version',
        version='pipsalabim {:s}'.format(__version__),
        help='Print version and exit.')
    parser.add_argument(
        '-l', '--loglevel', default='WARNING',
        help='Logger verbosity level (default: WARNING).')
    subparsers = parser.add_subparsers(title='commands')

    report_parser = subparsers.add_parser('report')
    report_parser.set_defaults(command=report)

    update_parser = subparsers.add_parser('update')
    update_parser.set_defaults(command=update)

    args = parser.parse_args(argv)

    logger.start(args.loglevel)
    logger.info('Starting execution.')

    args.command(**vars(args))

    logger.info('Ending execution.')

    return 0


if __name__ == '__main__':
    try:
        status = main()
    except:
        logger.critical('shutting down due to fatal error')
        raise
    else:
        raise SystemExit(status)
