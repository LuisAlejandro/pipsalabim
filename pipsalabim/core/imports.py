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
``pipsalabim.core.imports`` studies the code searching for imports.

This module has advanced programming to inspect and locate imported
modules in python source code. It uses python's own Abstract Syntax
Trees (AST) to do such operations.
"""
from __future__ import absolute_import, print_function

import ast

from .logger import logger


class ImportVisitor(ast.NodeVisitor):
    """
    AST visitor for grabbing the import statements.

    ``ImportVisitor`` is a node visitor class that walks the abstract syntax
    tree and calls a visitor function for every import statement found.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the import node (lowercase). This visitor only has methods
    for processing ``Import`` and ``ImportFrom`` types of nodes. When any other
    type of node is entered, the `generic_visit` visitor is used instead.

    This visitor produces a list of tuples like::

        [
            ('MODULE', 'LEVEL'),
            ('MODULE', 'LEVEL'),
            ('MODULE', 'LEVEL'),
            ('MODULE', 'LEVEL'),
            ('MODULE', 'LEVEL')
        ]

    * ``MODULE``: a string containing the name of the imported module
                 (does not include the package to which it belongs).
    * ``LEVEL`` is the relative level of the imported module.

        - 0 is the level of a simple import like::

            import MODULE
            from MODULE import NAME

        - 1 is the level of a relative import in the same package,
          for example::

            import .MODULE
            from .MODULE import NAME
            from . import NAME

        - 2 is the level of a relative import in the parent package,
          for example::

            import ..MODULE
            from ..MODULE import NAME
            from .. import NAME
    """

    def __init__(self):
        """
        Initialize this ``ImportVisitor``.

        Sets initial empty values for ``self.modules`` which will help
        storing modules.

        :return: an ``ImportVisitor`` instance.

        .. versionadded:: 0.1.0
        """
        #: Attribute ``modules`` (list): Stores modules as they are found by
        #: the visitor methods.
        self.modules = []

    def visit(self, node):
        """
        Visit a node.

        :param node: an ``ast`` object representing a python statement.
        :return: a reference to ``visit_import`` if the node type is
                 ``Import``, to ``visit_importfrom`` if the node type is
                 ``ImportFrom`` or ``generic_visit`` for any other node.

        .. versionadded:: 0.1.0
        """
        if node.__class__.__name__ == 'Import':
            return self.visit_import(node)
        if node.__class__.__name__ == 'ImportFrom':
            return self.visit_importfrom(node)
        try:
            return self.generic_visit(node)
        except Exception:
            pass

    def visit_import(self, node):
        """
        Append node names to ``self.modules``.

        :param node: an ``ast`` object representing a python statement.

        .. versionadded:: 0.1.0
        """
        self.modules.extend((n.name, 0) for n in node.names)

    def visit_importfrom(self, node):
        """
        Append node names and levels to ``self.modules``.

        :param node: an ``ast`` object representing a python statement.

        .. versionadded:: 0.1.0
        """
        if node.module != '__future__':
            self.modules.append((node.module, node.level))


def parse_python_source(filename):
    """
    Parse the file ``filename`` and convert it to AST.

    :param filename: a string containing a path to a python source code file.
    :return: an AST object or ``None`` if the file has a syntax error.

    .. versionadded:: 0.1.0
    """
    try:
        with open(filename, 'rU') as p:
            return ast.parse(p.read())
    except Exception as e:
        logger.error('Error processing file "{0}": {1}'.format(filename, e))
        return None


def find_imports(package, filename):
    """
    Get a list of modules extracted from import statements.

    :param package: a string containing a python package to which ``filename``
                    belongs.
    :param filename: a string containing a path to a python source code file.
    :return: a list of modules in absolute form.

    .. versionadded:: 0.1.0
    """
    imports = []
    tree = parse_python_source(filename)
    visitor = ImportVisitor()
    visitor.visit(tree)

    for modname, level in visitor.modules:
        if not modname:
            modname = ''
        if level == 1:
            modname = '{0}.{1}'.format(package, modname)
        if level == 2:
            modname = '{0}.{1}'.format('.'.join(package.split('.')[:-1]),
                                       modname)
        imports.append(modname.strip('.'))
    return imports
