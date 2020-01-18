.. image:: https://gitcdn.xyz/repo/CollageLabs/pipsalabim/master/docs/_static/banner.svg

..

    Pip Sala Bim is an assistant to guess your pip dependencies from your code, without using a
    requirements file.

.. image:: https://img.shields.io/pypi/v/pipsalabim.svg
   :target: https://pypi.python.org/pypi/pipsalabim
   :alt: PyPI Package

.. image:: https://img.shields.io/travis/CollageLabs/pipsalabim.svg
   :target: https://travis-ci.org/CollageLabs/pipsalabim
   :alt: Travis CI

.. image:: https://coveralls.io/repos/github/CollageLabs/pipsalabim/badge.svg?branch=develop
   :target: https://coveralls.io/github/CollageLabs/pipsalabim?branch=develop
   :alt: Coveralls

.. image:: https://codeclimate.com/github/CollageLabs/pipsalabim/badges/gpa.svg
   :target: https://codeclimate.com/github/CollageLabs/pipsalabim
   :alt: Code Climate

.. image:: https://pyup.io/repos/github/CollageLabs/pipsalabim/shield.svg
   :target: https://pyup.io/repos/github/CollageLabs/pipsalabim/
   :alt: Updates

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://cla-assistant.io/readme/badge/CollageLabs/pipsalabim
   :target: https://cla-assistant.io/CollageLabs/pipsalabim
   :alt: Contributor License Agreement

.. image:: https://badges.gitter.im/CollageLabs/pipsalabim.svg
   :target: https://gitter.im/CollageLabs/pipsalabim
   :alt: Gitter Chat

|
|

.. _full documentation: https://pipsalabim.readthedocs.org
.. _PyPIContents: https://github.com/CollageLabs/pypicontents

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

    $ pip install --upgrade https://github.com/CollageLabs/pipsalabim/archive/master.tar.gz

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

.. _Gitter Chat: https://gitter.im/CollageLabs/pipsalabim
.. _StackOverflow: http://stackoverflow.com/questions/ask

If you have any doubts or problems, suscribe to our `Gitter Chat`_ and ask for help. You can also
ask your question on StackOverflow_ (tag it ``pipsalabim``) or drop me an email at luis@huntingbears.com.ve.

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

.. image:: https://rawcdn.githack.com/CollageLabs/pipsalabim/b00c6704253b9d05447b621f728869a2229d5322/docs/_static/promo-open-source.svg

.. _CollageLabsTwitter: https://twitter.com/CollageLabs
.. _CollageLabsGitHub: https://github.com/CollageLabs
.. _collagelabs.org: http://collagelabs.org

|

    Web collagelabs.org_ · GitHub `@CollageLabs`__ · Twitter `@CollageLabs`__

__ CollageLabsGitHub_
__ CollageLabsTwitter_

|
|

.. [#] AST refers to an Abstract Syntax Tree, you can read more on
       https://en.wikipedia.org/wiki/Abstract_syntax_tree