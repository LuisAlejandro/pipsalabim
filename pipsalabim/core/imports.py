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
Parsing and finding routines.
"""
from __future__ import absolute_import, print_function

import re

from snakefood.find import parse_python_source, get_ast_imports


def find_imports(package, py):
    "Yields a list of the module names the file 'py' depends on."

    ast, _ = parse_python_source(py)
    if ast is None:
        raise StopIteration

    found_imports = get_ast_imports(ast)
    if found_imports is None:
        raise StopIteration

    for modname, rname, lname, lineno, level, pragma in found_imports:
        content = open(py, 'r').read()
        if re.findall(r'__all__\s*=.*?%s.*' % modname, content):
            continue
        if level == 1:
            modname = '%s.%s' % (package, modname)
        if level == 2:
            modname = '%s.%s' % ('.'.join(package.split('.')[:-1]), modname)
        yield modname.strip('.')
