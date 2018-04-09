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
``pipsalabim.core.utils`` is a utility module.

This module contains several utilities to process information coming from the
other modules.
"""
from __future__ import absolute_import, print_function

import os
import sys
import fnmatch
from contextlib import contextmanager

if not sys.version_info < (3,):
    unicode = str
    basestring = str


def u(u_string):
    """
    Convert a string to unicode working on both python 2 and 3.

    :param u_string: a string to convert to unicode.

    .. versionadded:: 0.1.5
    """
    if isinstance(u_string, unicode):
        return u_string
    return u_string.decode('utf-8')


def s(s_string):
    """
    Convert a byte stream to string working on both python 2 and 3.

    :param s_string: a byte stream to convert to string.

    .. versionadded:: 0.1.5
    """
    if isinstance(s_string, bytes):
        return s_string
    return s_string.encode('utf-8')


@contextmanager
def custom_sys_path(new_sys_path):
    """
    Context manager to momentarily change ``sys.path``.

    :param new_sys_path: a list of paths to overwrite ``sys.path``.

    .. versionadded:: 0.1.0
    """
    old_sys_path = sys.path
    sys.path = new_sys_path
    yield
    sys.path = old_sys_path


@contextmanager
def remove_sys_modules(remove):
    """
    Context manager to momentarily remove modules from ``sys.modules``.

    :param remove: a list of modules to remove from ``sys.modules``.

    .. versionadded:: 0.1.0
    """
    old_sys_modules = sys.modules
    for r in remove:
        if r in sys.modules:
            del sys.modules[r]
    yield
    sys.modules = old_sys_modules


def list_files(path=None, pattern='*'):
    """
    List files on ``path`` (non-recursively).

    Locate all the files matching the supplied filename pattern in the first
    level of the supplied ``path``. If no pattern is supplied, all files will
    be returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within the first level of
             path (non-recursive).

    .. versionadded:: 0.1.0
    """
    assert isinstance(path, basestring)
    assert isinstance(pattern, basestring)

    filelist = []
    for f in fnmatch.filter(os.listdir(path), pattern):
        if os.path.isfile(os.path.join(path, f)):
            filelist.append(os.path.join(path, f))
    return filelist


def find_files(path=None, pattern='*'):
    """
    Locate all the files matching the supplied ``pattern`` in ``path``.

    Locate all the files matching the supplied filename pattern in and below
    the supplied root directory. If no pattern is supplied, all files will be
    returned.

    :param path: a string containing a path where the files will be looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of files matching the pattern within path (recursive).

    .. versionadded:: 0.1
    """
    assert isinstance(path, basestring)
    assert isinstance(pattern, basestring)

    filelist = []
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for filename in fnmatch.filter(files, pattern):
            if os.path.isfile(os.path.join(directory, filename)):
                filelist.append(os.path.join(directory, filename))
    return filelist


def is_valid_path(path):
    """
    Test if ``path`` is a valid python path.

    :param path: a string containing a path.
    :return: ``True`` if ``path`` is a valid python path. ``False``
             otherwise.

    .. versionadded:: 0.1.0
    """
    for component in os.path.normpath(path).split(os.sep):
        if ('.' in component or '-' in component) and \
           component not in ['.', '..']:
            return False
    return True


def chunk_report(downloaded, total):
    """
    Print the progress of a download.

    :param downloaded: an integer representing the size (in bytes) of data
                       downloaded so far.
    :param total: an integer representing the total size (in bytes) of data
                  that needs to be downloaded.

    .. versionadded:: 0.1.0
    """
    percent = round((float(downloaded) / total) * 100, 2)
    sys.stdout.write(('Downloaded {0:0.0f} of {1:0.0f} kB '
                      '({2:0.0f}%)\r').format(downloaded / 1024,
                                              total / 1024, percent))
    if downloaded >= total:
        sys.stdout.write('\n\n')


def chunk_read(response, chunk_size=8192, report_hook=None):
    """
    Download a file by chunks.

    :param response: a file object as returned by ``urlopen``.
    :param chunk_size: an integer representing the size of the chunks to be
                       downloaded at a time.
    :param report_hook: a function to report the progress of the download.
    :return: a blob containing the downloaded file.

    .. versionadded:: 0.1.0
    """
    data = u('')
    downloaded = 0
    total = int(response.info().get('Content-Length').strip())

    while True:
        chunk = response.read(chunk_size)

        if not chunk:
            break

        data += u(chunk)
        downloaded += len(chunk)

        if report_hook:
            report_hook(downloaded, total)

    return data


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
