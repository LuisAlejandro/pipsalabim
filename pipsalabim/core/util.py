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

try:
    basestring
except NameError:
    basestring = str


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


def find_dirs(path=None, pattern='*'):
    """
    Search for directories (recursive).

    Locate all the directories matching the supplied pattern in and below
    the supplied root directory. If no pattern is supplied, all directories
    will be returned. The result includes ``path``.

    :param path: a string containing a path where the directories will be
                 looked for.
    :param pattern: a string containing a regular expression.
    :return: a list of directories matching the pattern within path
             (recursive).

    .. versionadded:: 0.1.0
    """
    assert isinstance(path, basestring)
    assert isinstance(pattern, basestring)

    dirlist = [path]
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for subdir in fnmatch.filter(subdirs, pattern):
            if os.path.isdir(os.path.join(directory, subdir)):
                dirlist.append(os.path.join(directory, subdir))
    return dirlist


def is_valid_path(path):
    """
    Test if ``subpath`` is a subdirectory of ``path``.

    :param subpath: a string containing a path.
    :param path: a string containing a path.
    :return: ``True`` if ``subpath`` is contained within ``path``. ``False``
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
    sys.stdout.write(('Downloaded {:d} of {:d} kB '
                      '({:0.2f}%)\r').format(downloaded / 60,
                                             total / 60, percent))
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
    data = []
    downloaded = 0
    total = int(response.info().getheader('Content-Length').strip())

    while True:
        chunk = response.read(chunk_size)

        if not chunk:
            break

        data += chunk
        downloaded += len(chunk)

        if report_hook:
            report_hook(downloaded, total)

    return ''.join(data)
