.. image:: https://raw.githubusercontent.com/LuisAlejandro/pipsalabim/develop/docs/_static/banner.svg

..

    Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
    requirements file.

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
   :target: https://pypi.org/project/pipsalabim
   :alt: PyPI Package

.. image:: https://img.shields.io/github/release/LuisAlejandro/pipsalabim.svg
   :target: https://github.com/LuisAlejandro/pipsalabim/releases
   :alt: Github Releases

.. image:: https://img.shields.io/github/issues/LuisAlejandro/pipsalabim
   :target: https://github.com/LuisAlejandro/pipsalabim/issues?q=is%3Aopen
   :alt: Github Issues

.. image:: https://github.com/LuisAlejandro/pipsalabim/workflows/Push/badge.svg
   :target: https://github.com/LuisAlejandro/pipsalabim/actions?query=workflow%3APush
   :alt: Push

.. image:: https://coveralls.io/repos/github/LuisAlejandro/pipsalabim/badge.svg?branch=develop
   :target: https://coveralls.io/github/LuisAlejandro/pipsalabim?branch=develop
   :alt: Coverage

.. image:: https://cla-assistant.io/readme/badge/LuisAlejandro/pipsalabim
   :target: https://cla-assistant.io/LuisAlejandro/pipsalabim
   :alt: Contributor License Agreement

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://img.shields.io/discord/809504357359157288.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
   :target: https://discord.gg/6W6pJKRyAJ
   :alt: Discord Channel

|
|

.. _full documentation: https://pipsalabim.readthedocs.org
.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

Current version: 0.2.0

**Pip Sala Bim** will tell you which packages you need to install to satisfy the dependencies of
your project. It uses a simple *AST visitor* [#]_ for detecting imports and `PyPIContents`_ to
search which packages contain these imports.

For more information, please read the `full documentation`_.

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

Usage
-----

.. _USAGE.rst: USAGE.rst

See USAGE.rst_ for details.

Getting help
============

.. _Discord server: https://discord.gg/6W6pJKRyAJ
.. _StackOverflow: http://stackoverflow.com/questions/ask

If you have any doubts or problems, suscribe to our `Discord server`_ and ask for help. You can also
ask your question on StackOverflow_ (tag it ``pipsalabim``) or drop me an email at luis@collagelabs.org.

Contributing
============

.. _CONTRIBUTING.rst: CONTRIBUTING.rst

See CONTRIBUTING.rst_ for details.


Release history
===============

.. _HISTORY.rst: HISTORY.rst

See HISTORY.rst_ for details.

License
=======

.. _AUTHORS.rst: AUTHORS.rst
.. _GPL-3 License: LICENSE

Copyright 2016-2022, Pip Sala Bim Developers (read AUTHORS.rst_ for a full list of copyright holders).

Released under a `GPL-3 License`_.

Made with 💖 and 🍔
====================

.. image:: https://raw.githubusercontent.com/LuisAlejandro/pipsalabim/develop/docs/_static/author-banner.svg

.. _LuisAlejandroTwitter: https://twitter.com/LuisAlejandro
.. _LuisAlejandroGitHub: https://github.com/LuisAlejandro
.. _luisalejandro.org: https://luisalejandro.org

|

    Web luisalejandro.org_ · GitHub `@LuisAlejandro`__ · Twitter `@LuisAlejandro`__

__ LuisAlejandroGitHub_
__ LuisAlejandroTwitter_

|
|

.. [#] AST refers to an Abstract Syntax Tree, you can read more on
       https://en.wikipedia.org/wiki/Abstract_syntax_tree