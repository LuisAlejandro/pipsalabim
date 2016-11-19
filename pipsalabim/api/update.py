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
""" Implement the guess command.

"""
from __future__ import absolute_import, print_function

import os
import json
import pkgutil

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from ..core import (logger, find_imports, find_dirs,
                    list_files, create_file_if_notfound, is_subdir)


pypibranch = 'contents'
pypiurl = 'https://cdn.rawgit.com/LuisAlejandro/pypicontents'
stdlibjson = '%s/%s/stdlib.json' % (pypiurl, pypibranch)
pypijson = '%s/%s/contents.json' % (pypiurl, pypibranch)
stdlibjsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                              'stdlib.json')
pypijsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                            'contents.json')


def get_package_dirs(path):
    for i, n, p in pkgutil.walk_packages(find_dirs(path)):
        if p and isinstance(i, pkgutil.ImpImporter):
            if is_subdir(i.path, path):
                yield os.path.join(i.path, n), n


def get_packages(packagedirs, top_dir):
    for p, n in packagedirs:
        rpart = p.replace(os.path.dirname(top_dir), '')
        packagename = rpart.replace(os.sep, '.').strip('.')
        yield packagename, p


def get_local_modules(packages):
    modules = []
    for package, path in packages:
        for py in list_files(path, '*.py'):
            module = os.path.splitext(os.path.basename(py))[0]
            if module.startswith('__'):
                modules.append(package)
            else:
                modules.append('.'.join([package, module]))
    return sorted(set(modules))


def get_local_imports(packages):
    imports = []
    for package, path in packages:
        for py in list_files(path, '*.py'):
            imports.extend(find_imports(package, py))
    return imports


def get_local_packages(basedir):
    pdata = list(get_package_dirs(basedir))
    pdirs = os.path.commonprefix(list(map(lambda x: x[0], pdata)))
    return list(get_packages(pdata, pdirs))


def get_stdlib_modules(stdlibjson):
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


def get_pypicontents_modules(pypijson):
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


def get_dependencies(contents, module):
    for pkg, data in contents.items():
        for mod in data['modules']:
            if mod == module:
                yield pkg


def main(**kwargs):
    """ Execute the command.

    """

    foundreqs = []
    notfoundmod = []
    basedir = os.getcwd()

    stdlib_modules = get_stdlib_modules(stdlibjson)
    pypi_modules = get_pypicontents_modules(pypijson)

    local_packages = get_local_packages(basedir)
    local_modules = get_local_modules(local_packages)
    local_imports = get_local_imports(local_packages)

    satisfied = stdlib_modules + local_modules
    unsatisfied = set(local_imports) - set(satisfied)

    for mod in unsatisfied:
        options = list(get_dependencies(pypi_modules, mod))

        if len(options) > 1:
            print('There is more than one PyPI package that satisfies this module: %s' % mod)

            while True:
                print('\nPlease write the one you would like to use.')
                for o in options:
                    print('    - %s' % o)

                selected = raw_input('\n>> ')
                if selected not in options:
                    print('"%s" not available.' % selected)
                    continue

                foundreqs.append(selected)
                break

        elif len(options) == 0:
            notfoundmod.append(mod)

        elif len(options) == 1:
            foundreqs.extend(options)

    if foundreqs:
        print('\nThese are the PyPI packages you need to install to satisfy dependencies:')
        for f in foundreqs:
            print('    - %s' % f)

    else:
        print('\nYour dependencies are satisfied by the standard library and internal code.')
        print('Congratulations!')

    if notfoundmod:
        print('\nWe couldnt find these python modules in any PyPI package, sorry:')
        for n in notfoundmod:
            print('    - %s' % n)

    return 0
