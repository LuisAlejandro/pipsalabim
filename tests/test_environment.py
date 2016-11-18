#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import doctest
import unittest
from contextlib import contextmanager

from pipsalabim.environment import Environment

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out

class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')
        self.odoo_beginners_dir = os.path.join(self.exampledir, 'odoo-beginners')
        self.odoo = Environment()

    def tearDown(self):
        self.odoo.destroy()

    def bundle_name_list(self, environment):
        for bundle in environment.bundles:
            yield bundle.name

    def test_01_initialization(self):
        self.assertListEqual(sorted(list(self.bundle_name_list(self.odoo))),
                             sorted(['addons', 'addons']))

    def test_02_addbundles(self):
        self.odoo.addbundles([self.odoo_afr_dir, self.odoo_beginners_dir], False)
        self.assertListEqual(sorted(list(self.bundle_name_list(self.odoo))),
                             sorted(['addons', 'addons', 'addons-vauxoo', 'odoo-afr',
                                     'odoo-beginners']))

    def test_03_unexistent_record_ids(self):
        notmet_record_ids_should_be = [
            {'odoo-beginners': {
                'references_absent_ids/view/test.xml': ['unexistent_module']
                }
            }
        ]
        notmet_record_ids_report_should_be = (
            'The following record ids are not found in the environment:\n\n'
            '    Bundle: odoo-beginners\n'
            '    XML file: references_absent_ids/view/test.xml\n'
            '    Missing references:\n'
            '        - unexistent_module\n\n'
        )

        sys.exit = lambda *args: None
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_beginners_dir], False)
        self.assertListEqual(list(self.odoo.get_notmet_record_ids()),
                             notmet_record_ids_should_be)
        with capture(self.odoo.get_notmet_record_ids_report) as output:
            self.assertMultiLineEqual(notmet_record_ids_report_should_be,
                                      output)

    def test_04_unexistent_dependency(self):
        notmet_dependencies_should_be = [
            {'odoo-beginners': {
                'missing_dependency': ['unexistent_dependency']
                }
            }
        ]
        notmet_dependencies_report_should_be = (
            'The following module dependencies are not found in the environment:\n\n'
            '    Bundle: odoo-beginners\n'
            '    Module: missing_dependency\n'
            '    Missing dependencies:\n'
            '        - unexistent_dependency\n\n'
        )

        sys.exit = lambda *args: None
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_beginners_dir], False)
        self.assertListEqual(list(self.odoo.get_notmet_dependencies()),
                             notmet_dependencies_should_be)
        with capture(self.odoo.get_notmet_dependencies_report) as output:
            self.assertMultiLineEqual(notmet_dependencies_report_should_be,
                                      output)

    def test_05_satisfy_oca_dependencies(self):
        self.odoo.reset()
        self.odoo.addbundles([self.odoo_afr_dir], False)
        self.assertIn('addons-vauxoo', list(self.bundle_name_list(self.odoo)))


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('pipsalabim.environment'))
    return tests

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
