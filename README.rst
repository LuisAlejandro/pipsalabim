.. image:: https://gitcdn.xyz/repo/LuisAlejandro/pipsalabim/master/docs/_static/banner.svg

..

    Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
    requirements file.

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

|
|

.. [#] AST refers to an Abstract Syntax Tree, you can read more on
       https://en.wikipedia.org/wiki/Abstract_syntax_tree
.. _full documentation: https://pipsalabim.readthedocs.org
.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

**Pip Sala Bim** will tell you which packages you need to install to satisfy the dependencies of
your project. It uses a simple *AST visitor* [#]_ for detecting imports and `PyPIContents`_ to
search which packages contain these imports.

For more information, please read the `full documentation`_.

|

Getting started
===============

Installation
------------

.. _PyPI: https://pypi.python.org/pypi/pipsalabim

The ``pipsalabim`` program is written in python and hosted on PyPI_. Therefore, you can use
pip to install the stable version::

    $ pip install --upgrade pipsalabim

If you want to install the development version (not recomended), you can install
directlty from GitHub like this::

    $ pip install --upgrade https://github.com/LuisAlejandro/pipsalabim/archive/master.tar.gz

|

Usage
-----

``pipsalabim`` is really easy to use.

::

    $ cd your-python-project/
    $ pipsalabim report --help

    usage: pipsalabim report [-h] [-r]

    optional arguments:
      -h, --help          show this help message and exit
      -r, --requirements  Format output for requirements.txt file.

:sup:`You need to run *pipsalabim update* before being able to generate a report`

|

Contributing
============

Release history
===============

See `HISTORY.rst <HISTORY.rst>`_ for details.

|

License
=======

.. _AUTHORS.rst: AUTHORS.rst

Copyright 2016, Pip Sala Bim Developers (see `AUTHORS.rst <AUTHORS.rst>`_ for a full list of copyright holders).

Released under `GPL-3 License <LICENSE.rst>`_.

Authored and Maintained by Luis Martínez (`@LuisAlejandro <https://twitter.com/LuisAlejandro>`_) 

|

Made with :heart: and :hamburger:
=================================

.. image:: http://huntingbears.com.ve/static/img/site/banner.svg

.. _LuisAlejandro: https://github.com/LuisAlejandro
.. _Patreon: https://www.patreon.com/luisalejandro
.. _Flattr: https://flattr.com/profile/luisalejandro
.. _PayPal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B8LPXHQY8QE8Y

|

My name is Luis (`@LuisAlejandro <https://github.com/LuisAlejandro>`_) and I'm a Free and
Open-Source Software developer living in Maracay, Venezuela.

If you like what I do, please support me on Patreon_, Flattr_, or donate via PayPal_,
so that I can continue doing what I love.

    Blog `huntingbears.com.ve <http://huntingbears.com.ve/>`_ · 
    GitHub `@LuisAlejandro <https://github.com/LuisAlejandro>`_ · 
    Twitter `@LuisAlejandro <https://twitter.com/LuisAlejandro>`_