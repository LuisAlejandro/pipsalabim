"""
Parsing and finding routines.
This could be considered the core of snakefood, and where all the complexity lives.
"""
# This file is part of the Snakefood open source package.
# See http://furius.ca/snakefood/ for licensing details.

import re
import logging
import compiler
from compiler.visitor import ASTVisitor
from compiler.ast import Discard, Const, AssName, List, Tuple
from compiler.consts import OP_ASSIGN

ERROR_IMPORT = "    Line %d: Could not import module '%s'"
ERROR_SYMBOL = "    Line %d: Symbol is not a module: '%s'"
ERROR_UNUSED = "    Line %d: Ignored unused import: '%s'"
ERROR_SOURCE = "       %s"
WARNING_OPTIONAL = "    Line %d: Pragma suppressing import '%s'"


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
    #  The import statement uses the following convention: if a package's
    #  __init__.py code defines a list named __all__, it is taken to be the list
    #  of module names that should be imported when from package import * is
    #  encountered. It is up to the package author to keep this list up-to-date
    #  when a new version of the package is released. Package authors may also
    #  decide not to support it, if they don't see a use for importing * from
    #  their package.
    def visitAssign(self, node):
        lhs = node.nodes
        if (len(lhs) == 1 and
            isinstance(lhs[0], AssName) and
            lhs[0].name == '__all__' and
            lhs[0].flags == OP_ASSIGN):

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


class ImportWalker(ASTVisitor):
    "AST walker that we use to dispatch to a default method on the visitor."

    def __init__(self, visitor):
        ASTVisitor.__init__(self)
        self._visitor = visitor

    def default(self, node, *args):
        self._visitor.default(node)
        ASTVisitor.default(self, node, *args)


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
        logging.error("Could not read file '%s'." % fn)
        return None, None

    # Convert the file to an AST.
    try:
        ast = compiler.parse(contents)
    except SyntaxError, e:
        err = '%s:%s: %s' % (fn, e.lineno or '--', e.msg)
        logging.error("Error processing file '%s':\n%s" %
                      (fn, err))
        return None, lines
    except TypeError, e:
        # Note: this branch untested, applied from a user-submitted patch.
        err = '%s: %s' % (fn, str(e))
        logging.error("Error processing file '%s':\n%s" %
                      (fn, err))
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


def find_imports(fn):
    "Yields a list of the module names the file 'fn' depends on."

    ast, _ = parse_python_source(fn)
    if ast is None:
        raise StopIteration

    found_imports = get_ast_imports(ast)
    if found_imports is None:
        raise StopIteration

    # local_modules = 

    for modname, rname, lname, lineno, _, _ in found_imports:
        content = open(fn, 'r').read()
        if re.findall(r'from\s*(?:\.\.|\.)%s\s*import.*?(?:%s|\*).*' % (modname, rname), content):
            continue
        if not rname and re.findall(r'__all__\s*=.*?%s' % modname, content):
            continue
        yield modname.split('.')[0]
