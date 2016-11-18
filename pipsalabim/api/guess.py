""" Implement the guess command.

"""
from __future__ import absolute_import
from __future__ import print_function

import os
import json
import pkgutil

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from ..core import logger, find_files, find_imports, find_dirs, list_files, create_file_if_notfound


pypibranch = 'contents'
pypiurl = 'https://cdn.rawgit.com/LuisAlejandro/pypicontents'
stdlibjson = '%s/%s/stdlib.json' % (pypiurl, pypibranch)
pypijson = '%s/%s/contents.json' % (pypiurl, pypibranch)
stdlibjsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                              'stdlib.json')
pypijsonfile = os.path.join(os.environ.get('HOME'), '.cache', 'pipsalabim',
                            'contents.json')


def get_package_dirs(path):
    for i, n, p in pkgutil.walk_packages(find_dirs(path)):
        if p and isinstance(i, pkgutil.ImpImporter):
            yield os.path.join(i.path, n), n


def get_packages(packagedirs, top_dir):
    for p, n in packagedirs:
        rpart = p.replace(os.path.dirname(top_dir), '')
        packagename = rpart.replace(os.sep, '.').strip('.')
        yield packagename, p


def get_modules(packages):
    modules = []
    for package, path in packages:
        for py in list_files(path, '*.py'):
            module = os.path.splitext(os.path.basename(py))[0]
            if module.startswith('__'):
                modules.append(package)
            else:
                modules.append('.'.join([package, module]))
    return sorted(set(modules))


def get_local_imports(basedir):
    imports = []
    for py in find_files(basedir, '*.py'):
        imports.extend(find_imports(py))
    return imports


def get_local_modules(basedir):
    packagedirs = list(get_package_dirs(basedir))
    top_package_dir = os.path.commonprefix(list(map(lambda x: x[0], packagedirs)))
    packages = list(get_packages(packagedirs, top_package_dir))
    return get_modules(packages)


def get_stdlib_modules(stdlibjson):
    stdlibmods = []

    if not os.path.isfile(stdlibjsonfile):
        create_file_if_notfound(stdlibjsonfile)

        try:
            stdlibcont = urlopen(url=stdlibjson, timeout=10).read()
        except Exception as e:
            logger.error('download error: %s' % e)
            stdlibcont = '{}'

        with open(stdlibjsonfile, 'w') as s:
            s.write(stdlibcont.decode('utf-8'))

    with open(stdlibjsonfile, 'r') as s:
        stdlibdict = json.loads(s.read())

    for mods in stdlibdict.values():
        stdlibmods.extend(mods)

    return stdlibmods


def get_pypicontents_modules(pypijson):
    if not os.path.isfile(pypijsonfile):
        create_file_if_notfound(pypijsonfile)

        try:
            pypicont = urlopen(url=pypijson, timeout=10).read()
        except Exception as e:
            logger.error('download error: %s' % e)
            pypicont = '{}'

        with open(pypijsonfile, 'w') as s:
            s.write(pypicont.decode('utf-8'))

    with open(pypijsonfile, 'r') as s:
        pypidict = json.loads(s.read())

    return pypidict


def get_dependencies(contents, module):
    for pkg, data in contents.items():
        for mod in data['modules']:
            if mod == module:
                yield pkg


def main(**kwargs):
    """ Execute the command.

    """

    foundreqs = []
    notfoundmod = []
    basedir = os.getcwd()

    stdlib_modules = get_stdlib_modules(stdlibjson)
    pypi_modules = get_pypicontents_modules(pypijson)

    local_imports = get_local_imports(basedir)
    local_modules = get_local_modules(basedir)

    satisfied = stdlib_modules + local_modules
    unsatisfied = set(local_imports) - set(satisfied)

    for mod in unsatisfied:
        options = list(get_dependencies(pypi_modules, mod))

        if len(options) > 1:
            print('There is more than one package that satisfies this module: %s' % mod)

            while True:
                print('\nPlease write the one you would like to use.')
                for o in options:
                    print('    - %s' % o)

                selected = raw_input('\n>> ')
                if selected not in options:
                    print('"%s" not available.' % selected)
                    continue

                foundreqs.append(selected)
                break

        elif len(options) == 0:
            notfoundmod.append(mod)

        elif len(options) == 1:
            foundreqs.extend(options)

    if foundreqs:
        print('\nThese are the packages you need to install to satisfy dependencies:')
        for f in foundreqs:
            print('    - %s' % f)

    else:
        print('\nYour dependencies are satisfied by the standard library and internal code.')
        print('Congratulations!')

    if notfoundmod:
        print('\nWe couldnt find these modules in any package, sorry:')
        for n in notfoundmod:
            print('    - %s' % n)

    return 0
