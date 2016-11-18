# -*- coding: utf-8 -*-
#
#   This file is part of Pip Sala Bim
#   Copyright (C) 2016, Pip Sala Bim Developers
#   All rights reserved.
#
#   Please refer to AUTHORS.md for a complete list of Copyright
#   holders.
#
#   Pip Sala Bim is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Pip Sala Bim is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
""" Implementation of the command line interface.

"""
from __future__ import absolute_import

from argparse import ArgumentParser

from pipsalabim import __version__
from pipsalabim.api import guess
from pipsalabim.core import logger


def _cmdline(argv=None):
    """ Parse command line arguments.

    """
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="version",
            version="pipsalabim {:s}".format(__version__),
            help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARNING",
            help="logger warning level [WARNING]")
    subparsers = parser.add_subparsers(title="commands")
    guess_parser = subparsers.add_parser("guess")
    guess_parser.set_defaults(command=guess)
    args = parser.parse_args(argv)
    return args


def main(argv=None):
    """ Execute the application CLI.

    Arguments are taken from sys.argv by default.

    """
    args = _cmdline(argv)
    logger.start(args.warn)
    logger.info("starting execution")
    args.command(**vars(args))
    logger.info("successful completion")
    return 0

# Make the module executable.

if __name__ == "__main__":
    try:
        status = main()
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace
    else:
        raise SystemExit(status)
