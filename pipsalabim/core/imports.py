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
import ast
from ast import NodeVisitor, List, Tuple, Name, Store, Str, Expr

from .logger import logger


class ImportVisitor(NodeVisitor):
    """AST visitor for grabbing the import statements.

    This visitor produces a list of

       (module-name, remote-name, local-name, line-no, pragma)

    * remote-name is the name off the symbol in the imported module.
    * local-name is the name of the object given in the importing module.

    A node visitor base class that walks the abstract syntax tree and calls a
    visitor function for every node found.  This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the node.  So a `TryFinally` node visit function would
    be `visit_TryFinally`.  This behavior can be changed by overriding
    the `visit` method.  If no visitor function exists for a node
    (return value `None`) the `generic_visit` visitor is used instead.

    Don't use the `NodeVisitor` if you want to apply changes to nodes during
    traversing.  For this a special visitor exists (`NodeTransformer`) that
    allows modifications.
    """
    def __init__(self):
        self.modules = []
        self.recent = []

    def visit(self, node):
        """Visit a node."""
        method = 'visit_{0}'.format(node.__class__.__name__.lower())
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_import(self, node):
        self.accept_imports()
        self.recent.extend((x.name, None, x.asname or x.name, node.lineno, 0)
                           for x in node.names)

    def visit_importfrom(self, node):
        self.accept_imports()
        modname = node.module
        if modname == '__future__':
            return
        for alias in node.names:
            name, as_ = alias.name, alias.asname
            if name == '*':
                # We really don't know...
                mod = (modname, None, None, node.lineno, node.level)
            else:
                mod = (modname, name, as_ or name, node.lineno, node.level)
            self.recent.append(mod)

    def visit_assign(self, node):
        """
    # For package initialization files, try to fetch the __all__ list, which
    # implies an implicit import if the package is being imported via
    # from-import; from the documentation:
    #
    #  The import statement uses the following convention: if a package's
    #  __init__.py code defines a list named __all__, it is taken to be the
    #  list
    #  of module names that should be imported when from package import * is
    #  encountered. It is up to the package author to keep this list up-to-date
    #  when a new version of the package is released. Package authors may also
    #  decide not to support it, if they don't see a use for importing * from
    #  their package.

        """
        lhs = node.targets
        if len(lhs) == 1 and isinstance(lhs[0], Name) and \
           lhs[0].id == '__all__' and isinstance(lhs[0].ctx, Store):

            rhs = node.value
            if isinstance(rhs, (List, Tuple)):
                for namenode in rhs.elts:
                    # Note: maybe we should handle the case of non-consts.
                    if isinstance(namenode, Str):
                        modname = namenode.s
                        mod = (modname, None, modname, node.lineno, 0)
                        self.recent.append(mod)

    def generic_visit(self, node):
        pragma = None
        if self.recent and isinstance(node, Expr) and \
           isinstance(node.value, Str):
            const_node = node.value
            pragma = const_node.s

        self.accept_imports(pragma)
        super(ImportVisitor, self).generic_visit(node)

    def accept_imports(self, pragma=None):
        self.modules.extend((m, r, l, n, lvl, pragma)
                            for (m, r, l, n, lvl) in self.recent)
        self.recent = []

    def finalize(self):
        self.accept_imports()
        return self.modules


def parse_python_source(fn):
    """Parse the file 'fn' and return two things:

    1. The AST tree.
    2. A list of lines of the source line (typically used for verbose error
       messages).

    If the file has a syntax error in it, the first argument will be None.
    """
    # Read the file's contents to return it.
    # Note: we make sure to use universal newlines.
    try:
        contents = open(fn, 'rU').read()
        lines = contents.splitlines()
    except (IOError, OSError) as e:
        logger.error('Could not read file "{0}".'.format(fn))
        return None, None

    # Convert the file to an AST.
    try:
        ast_ = ast.parse(contents)
    except SyntaxError as e:
        err = '{0}:{1}: {2}'.format(fn, e.lineno or '--', e.msg)
        logger.error('Error processing file "{0}":\n{1}'.format(fn, err))
        return None, lines

    except TypeError as e:
        # Note: this branch untested, applied from a user-submitted patch.
        err = '{0}: {1}'.format(fn, str(e))
        logger.error('Error processing file "{0}":\n{1}'.format(fn, err))
        return None, lines

    return ast_, lines


def get_ast_imports(ast_):
    """
    Given an AST, return a list of module tuples for the imports found, in the
    form:
        (modname, remote-name, local-name, lineno, pragma)
    """
    assert ast_ is not None
    vis = ImportVisitor()
    vis.visit(ast_)
    found_imports = vis.finalize()
    return found_imports


def find_imports(package, py):
    "Yields a list of the module names the file 'py' depends on."

    imports = []
    ast, lines = parse_python_source(py)
    found_imports = get_ast_imports(ast)

    with open(py, 'r') as p:
        content = p.read()

    for modname, rname, lname, lineno, level, pragma in found_imports:
        if re.findall(r'__all__\s*=.*?{0}.*'.format(modname), content):
            continue
        if level == 2:
            package = '.'.join(package.split('.')[:-1])
        if level == 1 or level == 2:
            modname = '{0}.{1}'.format(package, modname)
        imports.append(modname.strip('.'))
    return imports
