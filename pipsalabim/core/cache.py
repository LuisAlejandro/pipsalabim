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
``pipsalabim.core.cache`` handles the download of `PyPIContents`_ cache.

.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

This module downlads and stores the json files needed to search for modules and
packages.
"""
from __future__ import absolute_import, print_function

import os
import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .logger import logger
from .util import chunk_report, chunk_read

stdliburl = ('https://raw.githubusercontent.com/LuisAlejandro/pypicontents/'
             'contents/stdlib.json')
pypiurl = ('https://raw.githubusercontent.com/LuisAlejandro/pypicontents/'
           'contents/pypi.json')
stdlibfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                          'stdlib.json')
pypifile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                        'pypi.json')


def download_json_database(datafile, dataurl):
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
            s.write(content.decode('utf-8'))
    except Exception as e:
        logger.error('I/O error: {0}'.format(e))
        return False
    return True


def get_database(filename, url):
    """
    Check if ``url`` has been downloaded and stored.

    :param filename: a string containing a path to store the contents of
                     the file downloaded from ``url``.
    :param url: a string containing a url to a file.
    :return: an interpreted json string.

    .. versionadded:: 0.1.0
    """
    if not os.path.isfile(filename) and \
       not download_json_database(filename, url):
        return []

    with open(filename, 'r') as s:
        return json.loads(s.read())
