# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.rst for a complete list of Copyright holders.
# Copyright (C) 2016-2022, Pip Sala Bim Developers.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

from setuptools import setup

from pipsalabim import (__author__, __email__, __version__, __url__,
                        __description__)


def read_requirements(reqfile):
    with open(reqfile, 'r') as r:
        reqs = filter(None, r.read().split('\n'))
    return [re.sub(r'\t*# pyup.*', r'', x) for x in reqs]


install_requires = read_requirements('requirements.txt')
tests_require = read_requirements('requirements.txt') + \
    read_requirements('requirements-dev.txt')

setup(
    name='pipsalabim',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    description=__description__,
    long_description=open('README.rst').read(),
    packages=['pipsalabim', 'pipsalabim.api', 'pipsalabim.core'],
    package_dir={'pipsalabim': 'pipsalabim'},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ('pipsalabim = pipsalabim.cli:main',),
    },
    license=open('LICENSE').read(),
    zip_safe=False,
    keywords=['pip', 'requirements.txt', 'guess', 'report'],
    platforms=['posix', 'linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    test_suite='tests',
    tests_require=tests_require
)
