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
""" Core implementation package.

"""
import os
import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from .logger import logger
from .util import chunk_report, chunk_read


pypibranch = 'contents'
pypiurl = 'https://raw.githubusercontent.com/LuisAlejandro/pypicontents'
stdlibjson = '%s/%s/stdlib.json' % (pypiurl, pypibranch)
pypijson = '%s/%s/pypi.json' % (pypiurl, pypibranch)
stdlibjsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                              'stdlib.json')
pypijsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                            'pypi.json')


def download_json_database(datafile, dataurl):

    if not os.path.isdir(os.path.dirname(datafile)):
        os.makedirs(os.path.dirname(datafile))

    try:
        response = urlopen(url=dataurl, timeout=10)
        content = chunk_read(response, report_hook=chunk_report)
    except Exception as e:
        logger.error('Download error: %s' % e)
        return False

    try:
        with open(datafile, 'w') as s:
            s.write(content.decode('utf-8'))
    except Exception as e:
        logger.error('I/O error: %s' % e)
        return False
    return True


def get_stdlib_modules():
    stdlibmods = []

    if not os.path.isfile(stdlibjsonfile) and \
       not download_json_database(stdlibjsonfile, stdlibjson):
        return stdlibmods

    with open(stdlibjsonfile, 'r') as s:
        stdlibdict = json.loads(s.read())

    for mods in stdlibdict.values():
        stdlibmods.extend(mods)

    return stdlibmods


def get_pypicontents_modules():
    if not os.path.isfile(pypijsonfile) and \
       not download_json_database(pypijsonfile, pypijson):
            return []

    with open(pypijsonfile, 'r') as s:
        return json.loads(s.read())
