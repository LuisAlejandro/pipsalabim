#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pipsalabim import (__author__, __email__, __version__, __url__,
                        __description__)

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
    install_requires=open('requirements.txt').read().split('\n'),
    entry_points={
        'console_scripts': ('pipsalabim = pipsalabim.cli:main',),
    },
    license=open('COPYING.rst').read(),
    zip_safe=False,
    keywords=['pip', 'requirements.txt', 'guess', 'report'],
    platforms=['posix', 'linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=open('requirements-dev.txt').read().split('\n')
)
