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
from .util import create_file_if_notfound


pypibranch = 'contents'
pypiurl = 'https://cdn.rawgit.com/LuisAlejandro/pypicontents'
stdlibjson = '%s/%s/stdlib.json' % (pypiurl, pypibranch)
pypijson = '%s/%s/contents.json' % (pypiurl, pypibranch)
stdlibjsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                              'stdlib.json')
pypijsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                            'contents.json')


def get_stdlib_modules():
    stdlibmods = []

    if not os.path.isfile(stdlibjsonfile):
        create_file_if_notfound(stdlibjsonfile)

        try:
            stdlibcont = urlopen(url=stdlibjson, timeout=10).read()
        except Exception as e:
            logger.error('download error: %s' % e)
            stdlibcont = '{}'

        with open(stdlibjsonfile, 'w') as s:
            s.write(stdlibcont.decode('utf-8'))

    with open(stdlibjsonfile, 'r') as s:
        stdlibdict = json.loads(s.read())

    for mods in stdlibdict.values():
        stdlibmods.extend(mods)

    return stdlibmods


def get_pypicontents_modules():
    if not os.path.isfile(pypijsonfile):
        create_file_if_notfound(pypijsonfile)

        try:
            pypicont = urlopen(url=pypijson, timeout=10).read()
        except Exception as e:
            logger.error('download error: %s' % e)
            pypicont = '{}'

        with open(pypijsonfile, 'w') as s:
            s.write(pypicont.decode('utf-8'))

    with open(pypijsonfile, 'r') as s:
        pypidict = json.loads(s.read())

    return pypidict
