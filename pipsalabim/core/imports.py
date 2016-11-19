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
import compiler
from compiler.visitor import ASTVisitor
from compiler.ast import Discard, Const, AssName, List, Tuple
from compiler.consts import OP_ASSIGN

from .logger import logger


class ImportWalker(ASTVisitor):
    "AST walker that we use to dispatch to a default method on the visitor."

    def __init__(self, visitor):
        ASTVisitor.__init__(self)
        self._visitor = visitor

    def default(self, node, *args):
        self._visitor.default(node)
        ASTVisitor.default(self, node, *args)


class ImportVisitor(object):
    """AST visitor for grabbing the import statements.

    This visitor produces a list of

       (module-name, remote-name, local-name, line-no, pragma)

    * remote-name is the name off the symbol in the imported module.
    * local-name is the name of the object given in the importing module.
    """
    def __init__(self):
        self.modules = []
        self.recent = []

    def visitImport(self, node):
        self.accept_imports()
        self.recent.extend((x[0], None, x[1] or x[0], node.lineno, 0)
                           for x in node.names)

    def visitFrom(self, node):
        self.accept_imports()
        modname = node.modname
        if modname == '__future__':
            return
        for name, as_ in node.names:
            if name == '*':
                # We really don't know...
                mod = (modname, None, None, node.lineno, node.level)
            else:
                mod = (modname, name, as_ or name, node.lineno, node.level)
            self.recent.append(mod)

    # For package initialization files, try to fetch the __all__ list, which
    # implies an implicit import if the package is being imported via
    # from-import; from the documentation:
    #
    # The import statement uses the following convention: if a package's
    # __init__.py code defines a list named __all__, it is taken to be the list
    # of module names that should be imported when from package import * is
    # encountered. It is up to the package author to keep this list up-to-date
    # when a new version of the package is released. Package authors may also
    # decide not to support it, if they don't see a use for importing * from
    # their package.
    def visitAssign(self, node):
        lhs = node.nodes
        if len(lhs) == 1 and isinstance(lhs[0], AssName) and \
           lhs[0].name == '__all__' and lhs[0].flags == OP_ASSIGN:

            rhs = node.expr
            if isinstance(rhs, (List, Tuple)):
                for namenode in rhs:
                    # Note: maybe we should handle the case of non-consts.
                    if isinstance(namenode, Const):
                        modname = namenode.value
                        mod = (modname, None, modname, node.lineno, 0)
                        self.recent.append(mod)

    def default(self, node):
        pragma = None
        if self.recent:
            if isinstance(node, Discard):
                children = node.getChildren()
                if len(children) == 1 and isinstance(children[0], Const):
                    const_node = children[0]
                    pragma = const_node.value

        self.accept_imports(pragma)

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
    except (IOError, OSError), e:
        logger.error('Could not read file "%s".' % fn)
        return None, None

    # Convert the file to an AST.
    try:
        ast = compiler.parse(contents)
    except SyntaxError, e:
        err = '%s:%s: %s' % (fn, e.lineno or '--', e.msg)
        logger.error('Error processing file "%s":\n%s' % (fn, err))
        return None, lines

    except TypeError, e:
        # Note: this branch untested, applied from a user-submitted patch.
        err = '%s: %s' % (fn, str(e))
        logger.error('Error processing file "%s":\n%s' % (fn, err))
        return None, lines

    return ast, lines


def get_ast_imports(ast):
    """
    Given an AST, return a list of module tuples for the imports found, in the
    form:
        (modname, remote-name, local-name, lineno, pragma)
    """
    assert ast is not None
    vis = ImportVisitor()
    compiler.walk(ast, vis, ImportWalker(vis))
    found_imports = vis.finalize()
    return found_imports


def find_imports(package, py):
    "Yields a list of the module names the file 'py' depends on."

    ast, lines = parse_python_source(py)
    found_imports = get_ast_imports(ast)

    for modname, rname, lname, lineno, level, pragma in found_imports:
        content = open(py, 'r').read()
        if re.findall(r'__all__\s*=.*?%s.*' % modname, content):
            continue
        if level == 1:
            modname = '%s.%s' % (package, modname)
        if level == 2:
            modname = '%s.%s' % ('.'.join(package.split('.')[:-1]), modname)
        yield modname.strip('.')
