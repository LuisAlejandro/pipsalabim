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
``pipsalabim.api.report`` is a module implementing the report command.

This module contains the logic to examine your source code, extract internal
and external imports, and finally determine which external PyPI packages
you need to install in order to satisfy dependencies.
"""
from __future__ import absolute_import, print_function

import os
import pkgutil

from ..core.logger import logger
from ..core.imports import find_imports
from ..core.cache import get_stdlib_modules, get_pypicontents_modules
from ..core.util import find_dirs, list_files, is_subdir


def get_package_dirs(path):
    """
    List directories containing python packages on ``path``.

    :param path: a path pointing to a directory containing python code.
    :return: a list containing directories of packages.

    .. versionadded:: 0.1.0
    """
    package_dir = []
    for importer, pkgname, is_pkg in pkgutil.walk_packages(find_dirs(path)):
        if is_pkg and isinstance(importer, pkgutil.ImpImporter):
            if is_subdir(importer.path, path):
                package_dir.append(os.path.join(importer.path, pkgname))
    return package_dir


def get_local_packages(path):
    """
    List packages living in ``path`` with its directory.

    :param path: a path pointing to a directory containing python code.
    :return: a list of tuples containing the name of the package and
             the package directory. For example::

                 [
                    ('package_a', '/path/to/package_a'),
                    ('package_b.module_b', '/path/to/package_b/module_b'),
                    ('package_c.module_c', '/path/to/package_c/module_c')
                 ]

    .. versionadded:: 0.1.0
    """
    local_packages = []
    pkgdirs = get_package_dirs(path)
    topdir = os.path.commonprefix(pkgdirs)

    for pkgdir in pkgdirs:
        commondir = pkgdir.replace(os.path.dirname(topdir), '')
        pkgname = commondir.replace(os.sep, '.').strip('.')
        logger.debug('Found "%s" package in %s' % (pkgname, pkgdir))
        local_packages.append([pkgname, pkgdir])
    return local_packages


def get_local_modules(pkgdata):
    """
    List modules inside packages provided in ``pkgdata``.

    :param pkgdata: a list of tuples containing the name of a package and
                    the directory where its located.
    :return: a list of the modules according to the list of packages
             provided in ``pkgdata``.

    .. versionadded:: 0.1.0
    """
    local_modules = []
    for pkgname, pkgdir in pkgdata:
        for py in list_files(pkgdir, '*.py'):
            module = os.path.splitext(os.path.basename(py))[0]
            if not module.startswith('__'):
                modname = '.'.join([pkgname, module])
            else:
                modname = pkgname
            logger.debug('Found "%s" module.' % modname)
            local_modules.append(modname)
    return sorted(list(set(local_modules)))


def get_local_imports(pkgdata):
    """
    List modules imported inside of packages provided in ``pkgdata``.

    :param pkgdata: a list of tuples containing the name of a package and
                    the directory where its located.
    :return: a list of the modules imported according to the list of packages
             provided in ``pkgdata``.

    .. versionadded:: 0.1.0
    """
    imports = []
    for package, path in pkgdata:
        for py in list_files(path, '*.py'):
            imports.extend(find_imports(package, py))
    return imports


def get_dependencies(pypicontents, module):
    """
    List PyPI packages that provide ``module``.

    .. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

    :param pypicontents: a dictionary containing the `PyPIContents`_ index.
    :param module: a python module.
    :return: a list of PyPI packages that provide ``module``.

    .. versionadded:: 0.1.0
    """
    dependencies = []
    for pkgname, pkgdata in pypicontents.items():
        for mod in pkgdata['modules']:
            if mod == module:
                dependencies.append(pkgname)
    return dependencies


def main(*args, **kwargs):
    """
    Generate a report to inform about PyPI dependencies.

    :return: an exit status.

    .. versionadded:: 0.1.0
    """
    foundreqs = []
    notfoundmod = []
    basedir = os.getcwd()

    stdlib_modules = get_stdlib_modules()
    pypi_modules = get_pypicontents_modules()

    local_packages = get_local_packages(basedir)
    local_modules = get_local_modules(local_packages)
    local_imports = get_local_imports(local_packages)

    satisfied = stdlib_modules + local_modules
    unsatisfied = set(local_imports) - set(satisfied)

    for mod in unsatisfied:
        options = get_dependencies(pypi_modules, mod)

        if len(options) > 1:
            print(('There is more than one PyPI package that satisfies'
                   ' this module: %s') % mod)

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
        print(('\nThese are the PyPI packages you need to install to'
               ' satisfy dependencies:'))
        for f in foundreqs:
            print('    - %s' % f)

    else:
        print(('\nYour dependencies are satisfied by the standard library'
               ' and internal code.\nCongratulations!'))

    if notfoundmod:
        print(('\nWe couldnt find these python modules in any PyPI'
               ' package, sorry:'))
        for n in notfoundmod:
            print('    - %s' % n)

    return 0
