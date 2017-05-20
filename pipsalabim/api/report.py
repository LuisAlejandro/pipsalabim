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
import json
import pkgutil

from .. import __url__, stdlibfile, pypifile, libdir
from ..core.logger import logger
from ..core.imports import find_imports
from ..core.utils import (find_files, list_files, is_valid_path,
                          custom_sys_path, remove_sys_modules, fill_with_local,
                          fill_with_stdlib, fill_with_pypi)

from setuptools import find_packages

try:
    raw_input
except NameError:
    raw_input = input


def get_package_dirs(path):
    """
    List directories containing python packages on ``path``.

    :param path: a path pointing to a directory containing python code.
    :return: a list containing directories of packages.

    .. versionadded:: 0.1.0
    """
    package_dirs = []
    logger.info('Searching for package directories ...')
    for init in find_files(path, '__init__.py'):
        pkgdir = os.path.dirname(init)
        if os.path.commonprefix([pkgdir, path]) == path and \
           is_valid_path(os.path.relpath(pkgdir, path)):
            while True:
                init = os.path.split(init)[0]
                if not os.path.isfile(os.path.join(init, '__init__.py')):
                    break
            if init not in package_dirs:
                package_dirs.append(init)
    return package_dirs


def get_packages(path):
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
    packages = []
    package_dirs = get_package_dirs(path)
    logger.info('Extracting package names from directories ...')

    for _dir in package_dirs:
        for pkgname in find_packages(_dir):
            try:
                with custom_sys_path([_dir, libdir]):
                    with remove_sys_modules([pkgname]):
                        pkgdir = pkgutil.get_loader(pkgname).filename
            except Exception:
                pkgdir = os.path.join(_dir, os.sep.join(pkgname.split('.')))
            logger.debug('Found "{0}" package in '
                         '"{1}".'.format(pkgname, pkgdir))
            packages.append([pkgname, pkgdir])
    return packages


def get_modules(pkgdata):
    """
    List modules inside packages provided in ``pkgdata``.

    :param pkgdata: a list of tuples containing the name of a package and
                    the directory where its located.
    :return: a list of the modules according to the list of packages
             provided in ``pkgdata``.

    .. versionadded:: 0.1.0
    """
    modules = []
    logger.info('Extracting module names from packages ...')

    for pkgname, pkgdir in pkgdata:
        for py in list_files(pkgdir, '*.py'):
            module = os.path.splitext(os.path.basename(py))[0]
            if not module.startswith('__'):
                modname = '.'.join([pkgname, module])
            else:
                modname = pkgname
            logger.debug('Found "{0}" module in '
                         '"{1}" package.' .format(modname, pkgname))
            modules.append(modname)
    return sorted(list(set(modules)))


def get_imports(pkgdata):
    """
    List modules imported inside of packages provided in ``pkgdata``.

    :param pkgdata: a list of tuples containing the name of a package and
                    the directory where its located.
    :return: a list of the modules imported according to the list of packages
             provided in ``pkgdata``.

    .. versionadded:: 0.1.0
    """
    imports = []
    logger.info('Extracting imported modules from packages ...')

    for package, path in pkgdata:
        for filename in list_files(path, '*.py'):
            for i in find_imports(package, filename):
                logger.debug('Found import to "{0}" in "{1}"'
                             ' package.'.format(i, package))
                imports.append(i)
    return imports


def get_module_datadict(basedir):
    """
    Process the current directory to get data from packages and modules.

    :param basedir: a string containing a path to the directory to be analized.
    :return: a dictionary containing information for each imported module.
             Like::

                {
                    'module_a': ['LOCAL'],
                    'module_b': ['pypi_package_1'],
                    'module_c': ['pypi_package_1', 'pypi_package_2'],
                    'module_d': [],
                    'module_e': ['STDLIB2.6', 'STDLIB2.7', 'STDLIB3.5'],
                    'module_f': ['STDLIB2.7'],
                }

    .. versionadded:: 0.1.0
    """
    with open(stdlibfile, 'r') as s:
        stdlibdata = json.loads(s.read())

    with open(pypifile, 'r') as p:
        pypidata = json.loads(p.read())

    packages = get_packages(basedir)
    modules = get_modules(packages)
    imports = get_imports(packages)

    datadict = dict((m, []) for m in imports)
    datadict = fill_with_local(datadict, modules)
    datadict = fill_with_stdlib(datadict, stdlibdata)
    datadict = fill_with_pypi(datadict, pypidata)

    return datadict


def ask_multiple_pypi(datadict):
    """
    Ask the user about which PyPI package will use to satisfy an import.

    :param datadict: a dictionary containing modules as keys and
                     a list as values.
    :return: an updated ``datadict`` with the answered information from
             user.

    .. versionadded:: 0.1.0
    """
    for module, where in datadict.items():
        if len(where) < 2 or 'LOCAL' in where or \
           any('STDLIB' in s for s in where):
            continue

        print(('There is more than one PyPI package that satisfies'
               ' this module: {0}').format(module))

        while True:
            print('\nPlease write the one you would like to use.')
            for w in where:
                print('    - {0}'.format(w))

            selected = raw_input('\n>> ')
            if selected not in where:
                print('"{0}" not available.'.format(selected))
                continue

            datadict[module] = [selected]
            break

    return datadict


def get_messages(datadict):
    """
    Generate messages for each type of module in ``datadict``.

    :param datadict: a dictionary containing modules as keys and
                     a list as values.
    :return: a dictionary containing messages for each type of module.

    .. versionadded:: 0.1.0
    """
    msg = {'l': [], 's': [], 'n': [], 'p': []}
    for module, where in datadict.items():
        if 'LOCAL' in where:
            msg['l'].append(module)
        elif any('STDLIB' in s for s in where):
            msg['s'].append('{0}:{1}'.format(module, ','.join(sorted(where))))
        elif not where:
            msg['n'].append(module)
        else:
            msg['p'].append('{0}:{1}'.format(module, where[0]))
    return msg


def main(**kwargs):
    """
    Generate a report to inform about PyPI dependencies.

    .. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

    This command will search your code for unsatisfied dependencies by
    looking at your ``import`` statements. If an import is not satisfied by
    internal modules or the standard library, then it will query the
    PyPI module index provided by `PyPIContents`_.

    Sometimes, more than one PyPI package will provide the missing module and
    in such cases, you will be asked to select one from a list of options.

    If Pip Sala Bim fails to find a package providing the module you need, it
    will report it back to you.

    :return: an exit status.

    .. versionadded:: 0.1.0
    """
    basedir = os.getcwd()
    requirements = kwargs.get('requirements', False)

    if not os.path.isfile(pypifile) or not os.path.isfile(stdlibfile):
        print('You need to run "pipsalabim update" before trying to make a'
              ' report.')
        return 1

    if not os.path.isfile(os.path.join(basedir, 'setup.py')):
        print('Pip Sala Bim doesn\'t support folders without a setup.py.')
        return 1

    datadict = get_module_datadict(basedir)
    datadict = ask_multiple_pypi(datadict)
    messages = get_messages(datadict)

    if requirements:
        print('\nrequirements.txt file contents below')
        print('{0}>8{0}'.format('-' * 40))
        print('\n# file generated by Pip Sala Bim {0}'.format(__url__))
        print('\n'.join(m.split(':')[1] for m in messages['p']))
        return 0

    print('=' * 19)
    print('Pip Sala Bim Report')
    print('=' * 19)

    for msgtype, msgcont in messages.items():
        if not msgcont:
            continue
        if msgtype == 'l':
            print('\nThe folowing module imports have been found in your'
                  ' local source code:')
            print('\n'.join('    - {0}'.format(m) for m in msgcont))

        elif msgtype == 's':
            print('\nThe folowing module imports are part of python'
                  ' standard library:')
            for msg in msgcont:
                _mod, _py = msg.split(':')
                _py = _py.replace('STDLIB', '').split(',')
                _py = '{0} and {1}'.format(', '.join(_py[:-1]), _py[-1])
                print('    - {0} (python {1})'.format(_mod, _py))

        elif msgtype == 'p':
            print('\nThe folowing module imports where found in the PyPI'
                  ' module index:')
            print('\n'.join('    - {0} (available in "{1}" PyPI package. Use '
                            '"pip install {1}"'
                            ')'.format(*m.split(':')) for m in msgcont))
        elif msgtype == 'n':
            print('\nThe folowing module imports couldn\'t be found:')
            print('\n'.join('    - {0}'.format(m) for m in msgcont))

    if not messages['n'] and not messages['p']:
        print('\nCongratulations! All your imports are satisfied by the'
              ' python standard library or internal code.')

    return 0
