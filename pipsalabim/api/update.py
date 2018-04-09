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
``pipsalabim.api.update`` is a module implementing the update command.

Pip Sala Bim needs to keep a local copy of the PyPIContents database
to function properly. This command takes care of maintaining it
up-to-date.

Please note that this command must be executed manually.
"""
from __future__ import absolute_import, print_function

import os

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .. import stdliburl, pypiurl, stdlibfile, pypifile
from ..core.logger import logger
from ..core.utils import chunk_report, chunk_read, u


def download_json(datafile, dataurl):
    """
    Download a json file from ``dataurl``, store to ``datafile`` and report.

    :param datafile: a string containing a path to store the contents of
                     the file downloaded from ``dataurl``.
    :param dataurl: a string containing a url to a file.
    :return: ``True`` if operations went OK, ``False`` if not.

    .. versionadded:: 0.1.0
    """
    if not os.path.isdir(os.path.dirname(datafile)):
        os.makedirs(os.path.dirname(datafile))

    print(('{0} is not present, downloading '
           '...').format(os.path.basename(datafile)))

    try:
        response = urlopen(url=dataurl, timeout=10)
        content = chunk_read(response, report_hook=chunk_report)
    except Exception as e:
        logger.error('Download error: {0}'.format(e))
        return False

    try:
        with open(datafile, 'w') as s:
            s.write(u(content))
    except Exception as e:
        logger.error('I/O error: {0}'.format(e))
        return False
    return True


def main(**kwargs):
    """
    Update databases from PyPIContents.

    .. _stdlib.json: https://git.io/vXF1H
    .. _pypi.json: https://git.io/vXFDL
    .. _PyPIContents project: https://github.com/LuisAlejandro/pypicontents

    This function downloads the standard library modules index (`stdlib.json`_)
    and the PyPI modules index (`pypi.json`_) from the `PyPIContents project`_
    to keep a local copy of these files, which are critical to PiP Sala Bim.

    This command makes no comparing or checking prior to download.

    :return: an exit status.

    .. versionadded:: 0.1.0
    """
    print('Updating the standard library database ...')
    if download_json(stdlibfile, stdliburl):
        print('Success!\n')
    else:
        print('There was an error!\n')

    print('Updating the PyPIContents database ...')
    if download_json(pypifile, pypiurl):
        print('Success!\n')
    else:
        print('There was an error!\n')

    return 0
