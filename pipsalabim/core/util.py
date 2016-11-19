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
import os
import fnmatch


def get_path(path=None):
    """
    Build and normalize a path.

    This will resolve symlinks to their destination and convert
    relative to absolute paths. This function does not check if
    the python path really exists.

    :param path: a list with the components of a path.
    :return: a string indicating the full path.

    For example:

    >>> p = ['/usr', 'share', 'logs/vars', 'included', 'hola.txt']
    >>> get_path(p)
    '/usr/share/logs/vars/included/hola.txt'

    .. versionadded:: 0.1.0
    """
    path = path or []
    assert type(path) == list
    return os.path.normpath(os.path.realpath(
        os.path.abspath(os.path.join(*path))))


def list_files(path=None, pattern='*'):
    assert path
    assert type(path) == str
    files = fnmatch.filter(os.listdir(path), pattern)
    return [get_path([path, f]) for f in files
            if os.path.isfile(get_path([path, f]))]


def find_dirs(path=None, pattern='*'):
    d = []
    import fnmatch
    assert path
    assert pattern
    assert type(path) == str
    assert type(pattern) == str
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for subdir in fnmatch.filter(subdirs, pattern):
            if os.path.isdir(os.path.join(directory, subdir)):
                if os.path.islink(os.path.join(directory, subdir)):
                    d.append(os.path.join(get_path([directory]), subdir))
                else:
                    d.append(get_path([directory, subdir]))
    return d+[path]


def is_subdir(subpath, path):
    commonpath = os.path.commonprefix([os.path.realpath(subpath),
                                       os.path.realpath(path)])
    return commonpath == path


def create_file_if_notfound(filename):
    dedir = os.path.dirname(filename)
    if not os.path.isdir(dedir):
        os.makedirs(dedir)
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            os.utime(filename, None)
    return filename
