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

from .. import stdlibfile, pypifile, __url__
from ..core.logger import logger
from ..core.imports import find_imports
from ..core.util import find_dirs, list_files, is_valid_path

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
    for importer, pkgname, is_pkg in pkgutil.walk_packages(find_dirs(path)):
        if is_pkg and isinstance(importer, pkgutil.ImpImporter) and \
           os.path.commonprefix([importer.path, path]) == path and \
           is_valid_path(os.path.relpath(importer.path, path)):
            package_dirs.append(os.path.join(importer.path, pkgname))
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
    pkgdirs = get_package_dirs(path)
    topdir = os.path.commonprefix(pkgdirs)

    for pkgdir in pkgdirs:
        commondir = pkgdir.replace(os.path.dirname(topdir), '')
        pkgname = commondir.replace(os.sep, '.').strip('.')
        logger.debug('Found "{0}" package in {1}'.format(pkgname, pkgdir))
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
    for pkgname, pkgdir in pkgdata:
        for py in list_files(pkgdir, '*.py'):
            module = os.path.splitext(os.path.basename(py))[0]
            if not module.startswith('__'):
                modname = '.'.join([pkgname, module])
            else:
                modname = pkgname
            logger.debug('Found "{0}" module.' .format(modname))
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
    for package, path in pkgdata:
        for filename in list_files(path, '*.py'):
            imports.extend(find_imports(package, filename))
    return imports


def fill_with_local(datadict, modules):
    """
    Fill ``datadict`` if module is found in ``modules``.

    :param datadict: a dictionary containing modules as keys and
                     a list as values.
    :param modules: a list of modules present in the local python source code.
    :return: a dictionary containing information about the location of each
             imported module.

    .. versionadded:: 0.1.0
    """
    for module, where in datadict.items():
        if not where and module in modules:
            datadict[module].append('LOCAL')
    return datadict


def fill_with_stdlib(datadict, stdlibdata):
    """
    Fill ``datadict`` with modules from ``stdlibdata`` if found.

    :param datadict: a dictionary containing modules as keys and
                     a list as values.
    :param stdlibdata: a dictionary containing the modules of the standard
                       library of each python version.
    :return: a dictionary containing information about the location of each
             imported module.

    .. versionadded:: 0.1.0
    """
    for module, where in datadict.items():
        if where:
            continue
        for version, mods in stdlibdata.items():
            if module not in mods:
                continue
            datadict[module].append('STDLIB{0}'.format(version))
    return datadict


def fill_with_pypi(datadict, pypidata):
    """
    Fill ``datadict`` with modules from ``pypidata`` if found.

    .. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

    :param datadict: a dictionary containing modules as keys and
                     a list as values.
    :param pypidata: a dictionary with the `PyPIContents`_ database.
    :return: an updated dictionary containing information about the location
             of each imported module.

    .. versionadded:: 0.1.0
    """
    for module, where in datadict.items():
        if where:
            continue
        for package, data in pypidata.items():
            if module not in data['modules']:
                continue
            datadict[module].append(package)
    return datadict


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

    datadict = {m: [] for m in imports}
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

    datadict = get_module_datadict(basedir)
    datadict = ask_multiple_pypi(datadict)
    messages = get_messages(datadict)

    if requirements:
        print('\nrequirements.txt file contents below')
        print('-' * 50)
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
            print('\nThe folowing module imports couldnt be found:')
            print('\n'.join('    - {0}'.format(m) for m in msgcont))

    if not messages['n'] and not messages['p']:
        print('\nCongratulations! All your imports are satisfied by the'
              ' python standard library or internal code.')

    return 0
