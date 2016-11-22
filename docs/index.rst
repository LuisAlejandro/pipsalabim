.. image:: https://gitcdn.xyz/repo/LuisAlejandro/pipsalabim/master/docs/_static/title.svg

-----

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
   :target: https://pypi.python.org/pypi/pipsalabim
   :alt: PyPI Package

.. image:: https://img.shields.io/travis/LuisAlejandro/pipsalabim.svg
   :target: https://travis-ci.org/LuisAlejandro/pipsalabim
   :alt: Travis CI

.. image:: https://coveralls.io/repos/github/LuisAlejandro/pipsalabim/badge.svg?branch=master
   :target: https://coveralls.io/github/LuisAlejandro/pipsalabim?branch=master
   :alt: Coveralls

.. image:: https://codeclimate.com/github/LuisAlejandro/pipsalabim/badges/gpa.svg
   :target: https://codeclimate.com/github/LuisAlejandro/pipsalabim
   :alt: Code Climate

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://badges.gitter.im/LuisAlejandro/pipsalabim.svg
   :target: https://gitter.im/LuisAlejandro/pipsalabim
   :alt: Gitter Chat

Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
requirements file.

Pip Sala Bim will tell you which packages you need to install to satisfy the dependencies of
your project. It uses a simple AST visitor for detecting imports and `PyPIContents`_ to
search which packages contain these imports.

* Free software: GPL-3
* Documentation: https://pipsalabim.readthedocs.org

.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   contributing
   authors
   history
