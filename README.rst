.. image:: https://rawcdn.githack.com/LuisAlejandro/pipsalabim/8f880530063f05e96d006a55b5c5f4afee9c5e40/docs/_static/banner.svg

..

    Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
    requirements file.

.. image:: https://img.shields.io/github/release/LuisAlejandro/pipsalabim.svg
   :target: https://github.com/LuisAlejandro/pipsalabim/releases
   :alt: Github Releases

.. image:: https://img.shields.io/github/issues/LuisAlejandro/pipsalabim
   :target: https://github.com/LuisAlejandro/pipsalabim/issues?q=is%3Aopen
   :alt: Github Issues

.. image:: https://github.com/LuisAlejandro/pipsalabim/workflows/Push/badge.svg
   :target: https://github.com/LuisAlejandro/pipsalabim/actions?query=workflow%3APush
   :alt: Push

.. image:: https://codeclimate.com/github/LuisAlejandro/pipsalabim/badges/gpa.svg
   :target: https://codeclimate.com/github/LuisAlejandro/pipsalabim
   :alt: Code Climate

.. image:: https://snyk.io/test/github/LuisAlejandro/pipsalabim/badge.svg
   :target: https://snyk.io/test/github/LuisAlejandro/pipsalabim
   :alt: Snyk

.. image:: https://cla-assistant.io/readme/badge/LuisAlejandro/pipsalabim
   :target: https://cla-assistant.io/LuisAlejandro/pipsalabim
   :alt: Contributor License Agreement

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
   :target: https://pypi.python.org/pypi/pipsalabim
   :alt: PyPI Package

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://img.shields.io/badge/chat-discord-ff69b4.svg
   :target: https://discord.gg/6W6pJKRyAJ
   :alt: Discord Channel

|
|

.. _full documentation: https://pipsalabim.readthedocs.org
.. _PyPIContents: https://github.com/LuisAlejandro/pypicontents

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

``pipsalabim`` is really easy to use. Go to your python project and execute it as follows to
start guessing your dependencies::

    $ cd your-python-project/
    $ pipsalabim report --help

    usage: pipsalabim report [-h] [-r]

    optional arguments:
      -h, --help          show this help message and exit
      -r, --requirements  Format output for requirements.txt file.

:sup:`You need to run "pipsalabim update" before being able to generate a report.`

Getting help
============

.. _Gitter Chat: https://gitter.im/LuisAlejandro/pipsalabim
.. _StackOverflow: http://stackoverflow.com/questions/ask

If you have any doubts or problems, suscribe to our `Gitter Chat`_ and ask for help. You can also
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

.. _COPYING.rst: COPYING.rst
.. _AUTHORS.rst: AUTHORS.rst
.. _GPL-3 License: LICENSE.rst

Copyright 2016, Pip Sala Bim Developers (read AUTHORS.rst_ for a full list of copyright holders).

Released under a `GPL-3 License`_ (read COPYING.rst_ for license details).

Made with :heart: and :hamburger:
=================================

.. image:: https://rawcdn.githack.com/LuisAlejandro/pipsalabim/8f880530063f05e96d006a55b5c5f4afee9c5e40/docs/_static/promo-open-source.svg

.. _LuisAlejandroTwitter: https://twitter.com/LuisAlejandro
.. _LuisAlejandroGitHub: https://github.com/LuisAlejandro
.. _collagelabs.org: http://collagelabs.org

|

    Web collagelabs.org_ · GitHub `@LuisAlejandro`__ · Twitter `@LuisAlejandro`__

__ LuisAlejandroGitHub_
__ LuisAlejandroTwitter_

|
|

.. [#] AST refers to an Abstract Syntax Tree, you can read more on
       https://en.wikipedia.org/wiki/Abstract_syntax_tree