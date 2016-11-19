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
""" Global application logging.

All modules use the same global logging object. No messages will be emitted
until the logger is started.

"""
from __future__ import absolute_import

import logging


class _Logger(logging.Logger):
    """ Log messages to STDERR.

    """
    LOGFMT = "%(asctime)s;%(levelname)s;%(name)s;%(msg)s"

    def __init__(self, name=None):
        """ Initialize this logger.

        The name defaults to the application name. Loggers with the same name
        refer to the same underlying object. Names are hierarchical, e.g.
        'parent.child' defines a logger that is a descendant of 'parent'.

        """
        super(_Logger, self).__init__(name or __name__.split(".")[0])
        self.addHandler(logging.NullHandler())  # default to no output
        self.active = False
        return

    def start(self, level="WARN"):
        """ Start logging with this logger.

        Until the logger is started, no messages will be emitted. This applies
        to all loggers with the same name and any child loggers.

        Messages less than the given priority level will be ignored. The
        default level is 'WARN', which conforms to the *nix convention that a
        successful run should produce no diagnostic output. Available levels
        and their suggested meanings:

          DEBUG - output useful for developers
          INFO - trace normal program flow, especially external interactions
          WARN - an abnormal condition was detected that might need attention
          ERROR - an error was detected but execution continued
          CRITICAL - an error was detected and execution was halted

        """
        if self.active:
            return
        handler = logging.StreamHandler()  # stderr
        handler.setFormatter(logging.Formatter(self.LOGFMT))
        self.addHandler(handler)
        self.setLevel(level.upper())
        self.active = True
        return

    def stop(self):
        """ Stop logging with this logger.

        """
        if not self.active:
            return
        self.removeHandler(self.handlers[-1])
        self.active = False
        return


logger = _Logger()
