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

.. image:: https://pyup.io/repos/github/LuisAlejandro/pipsalabim/shield.svg
   :target: https://pyup.io/repos/github/LuisAlejandro/pipsalabim/
   :alt: Updates

.. image:: https://readthedocs.org/projects/pipsalabim/badge/?version=latest
   :target: https://readthedocs.org/projects/pipsalabim/?badge=latest
   :alt: Read The Docs

.. image:: https://cla-assistant.io/readme/badge/LuisAlejandro/pipsalabim
   :target: https://cla-assistant.io/LuisAlejandro/pipsalabim
   :alt: Contributor License Agreement

.. image:: https://badges.gitter.im/LuisAlejandro/pipsalabim.svg
   :target: https://gitter.im/LuisAlejandro/pipsalabim
   :alt: Gitter Chat

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

.. image:: http://huntingbears.com.ve/static/img/site/banner.svg

.. _Patreon: https://www.patreon.com/luisalejandro
.. _Flattr: https://flattr.com/profile/luisalejandro
.. _PayPal: https://www.paypal.me/martinezfaneyth
.. _LuisAlejandroTwitter: https://twitter.com/LuisAlejandro
.. _LuisAlejandroGitHub: https://github.com/LuisAlejandro
.. _huntingbears.com.ve: http://huntingbears.com.ve

|

My name is Luis (`@LuisAlejandro`__) and I'm a Free and
Open-Source Software developer living in Maracay, Venezuela.

__ LuisAlejandroTwitter_

If you like what I do, please support me on Patreon_, Flattr_, or donate via PayPal_,
so that I can continue doing what I love.

    Blog huntingbears.com.ve_ · GitHub `@LuisAlejandro`__ · Twitter `@LuisAlejandro`__

__ LuisAlejandroGitHub_
__ LuisAlejandroTwitter_

|
|

.. [#] AST refers to an Abstract Syntax Tree, you can read more on
       https://en.wikipedia.org/wiki/Abstract_syntax_tree