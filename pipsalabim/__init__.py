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
``pipsalabim`` is just black magic.

Pip Sala Bim is a package that studies the codebase of your project in search
for internal and external imports. It then discards the imports that are
satisfied with internal code or with the standard library and finally
searches the `PyPIContents`_ index to list which packages satisfy your imports.

.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

"""
import os
from distutils import sysconfig


__author__ = 'Luis Alejandro Martínez Faneyth'
__email__ = 'luis@huntingbears.com.ve'
__version__ = '0.1.19'
__url__ = 'https://github.com/LuisAlejandro/pipsalabim'
__description__ = ('Pip Sala Bim is an assistant to guess your pip'
                   ' dependencies from your code, without using a'
                   ' requirements file.')
stdliburl = ('https://raw.githubusercontent.com/LuisAlejandro/pypicontents/'
             'contents/stdlib.json')
pypiurl = ('https://raw.githubusercontent.com/LuisAlejandro/pypicontents/'
           'contents/pypi.json')
stdlibfile = os.path.join(os.environ.get('HOME', os.path.expanduser('~')),
                          '.cache', 'pipsalabim', 'stdlib.json')
pypifile = os.path.join(os.environ.get('HOME', os.path.expanduser('~')),
                        '.cache', 'pipsalabim', 'pypi.json')
libdir = sysconfig.get_python_lib(standard_lib=True)
