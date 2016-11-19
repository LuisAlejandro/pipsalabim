.. image:: https://cdn.rawgit.com/LuisAlejandro/pipsalabim/master/docs/_static/banner.svg

-----

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
           :target: https://pypi.python.org/pypi/pipsalabim

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
           :target: https://readthedocs.org/projects/pipsalabim/?badge=latest

.. image:: https://img.shields.io/travis/LuisAlejandro/pipsalabim.svg
           :target: https://travis-ci.org/LuisAlejandro/pipsalabim

.. image:: https://coveralls.io/repos/github/LuisAlejandro/pipsalabim/badge.svg?branch=master
           :target: https://coveralls.io/github/LuisAlejandro/pipsalabim?branch=master

.. image:: https://www.quantifiedcode.com/api/v1/project/6c2cc543a97c4d23988fc0463645c4f9/badge.svg
           :target: https://www.quantifiedcode.com/app/project/6c2cc543a97c4d23988fc0463645c4f9

Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
requirements file.

Pip Sala Bim will tell you which packages you need to install to satisfy the dependencies of
your project. It uses a simple AST visitor for detecting imports and `PyPIContents`_ to
search which packages contain these imports.

These words are magical, but be careful with what you play with ...

* Free software: GPL-3
* Documentation: https://pipsalabim.readthedocs.org

.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents
