#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
import doctest


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('pipsalabim.core.utils'))
    return tests


if __name__ == '__main__':
    sys.exit(unittest.main())
