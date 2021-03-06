.. image:: https://rawcdn.githack.com/CollageLabs/pipsalabim/8f880530063f05e96d006a55b5c5f4afee9c5e40/docs/_static/title.svg

-----

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
   :target: https://pypi.python.org/pypi/pipsalabim
   :alt: PyPI Package

.. image:: https://img.shields.io/travis/CollageLabs/pipsalabim.svg
   :target: https://travis-ci.org/CollageLabs/pipsalabim
   :alt: Travis CI

.. image:: https://coveralls.io/repos/github/CollageLabs/pipsalabim/badge.svg?branch=master
   :target: https://coveralls.io/github/CollageLabs/pipsalabim?branch=master
   :alt: Coveralls

.. image:: https://landscape.io/github/CollageLabs/pipsalabim/master/landscape.svg?style=flat
   :target: https://landscape.io/github/CollageLabs/pipsalabim/master
   :alt: Landscape

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://cla-assistant.io/readme/badge/CollageLabs/pipsalabim
   :target: https://cla-assistant.io/CollageLabs/pipsalabim
   :alt: Contributor License Agreement

.. image:: https://badges.gitter.im/CollageLabs/pipsalabim.svg
   :target: https://gitter.im/CollageLabs/pipsalabim
   :alt: Gitter Chat

.. _PyPIContents: https://github.com/CollageLabs/pypicontents

Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
requirements file.

Pip Sala Bim will tell you which packages you need to install to satisfy the dependencies of
your project. It uses a simple AST visitor for detecting imports and `PyPIContents`_ to
search which packages contain these imports.

* Free software: GPL-3
* Documentation: https://pipsalabim.readthedocs.org

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
   maintainer