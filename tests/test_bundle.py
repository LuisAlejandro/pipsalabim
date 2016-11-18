#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import doctest
import unittest

from pipsalabim.bundle import Bundle, Module


class TestModule(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.is_not_package_dir = os.path.join(self.exampledir, 'is-not-package',
                                               'is_not_package')
        self.openacademy_dir = os.path.join(self.exampledir, 'odoo-beginners',
                                            'openacademy')
        self.openacademy = Module(self.openacademy_dir)

    def test_01_has_manifest(self):
        self.assertEqual(self.openacademy.manifest,
                         os.path.join(self.openacademy_dir, '__openerp__.py'))

    def test_02_is_not_python_package(self):
        self.assertRaisesRegexp(
            AssertionError, 'The module is not a python package.',
            Module, self.is_not_package_dir
        )

    def test_03_match_properties(self):
        self.assertEqual(self.openacademy.properties.name, 'Open Academy')
        self.assertEqual(self.openacademy.properties.version, '0.1')
        self.assertListEqual(self.openacademy.properties.depends, ['base', 'board'])

    def test_04_get_record_ids_module_references(self):
        record_ids_should_be = [
            {'view/openacademy_course_view.xml': ['openacademy']},
            {'view/openacademy_session_view.xml': ['openacademy']},
            {'view/partner_view.xml': ['openacademy']},
            {'workflow/openacademy_session_workflow.xml': ['openacademy']},
            {'security/security.xml': ['openacademy']},
            {'view/openacademy_wizard_view.xml': ['openacademy']},
            {'view/openacademy_session_board.xml': ['openacademy']}
        ]

        if sys.version_info < (3,):
            self.assertCountEqual = self.assertItemsEqual
        self.assertCountEqual(list(self.openacademy.get_record_ids_module_references()),
                              record_ids_should_be)


class TestBundle(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.odoo_afr_dir = os.path.join(self.exampledir, 'odoo-afr')
        self.odoo_beginners_dir = os.path.join(self.exampledir, 'odoo-beginners')
        self.oca_deps_dir = os.path.join(self.exampledir, 'oca-deps')
        self.odoo_afr = Bundle(self.odoo_afr_dir, exclude_tests=False)
        self.odoo_beginners = Bundle(self.odoo_beginners_dir, exclude_tests=False)
        self.oca_deps = Bundle(self.oca_deps_dir, exclude_tests=False)

    def modules_slug_list(self, bundle):
        for module in bundle.modules:
            yield module.properties.slug

    def test_01_get_modules(self):
        odoo_afr_modules_should_be = ['account_afr_group_auditory',
                                      'account_financial_report']
        self.assertListEqual(sorted(list(self.modules_slug_list(self.odoo_afr))),
                             sorted(odoo_afr_modules_should_be))

    def test_02_modules_are_instances_of_module(self):
        for module in self.odoo_afr.modules:
            self.assertIsInstance(module, Module)

    def test_03_get_oca_dependencies(self):
        oca_dependencies_file_should_be = os.path.join(self.odoo_afr_dir,
                                                       'oca_dependencies.txt')
        self.assertEqual(self.odoo_afr.oca_dependencies_file,
                         oca_dependencies_file_should_be)

    def test_04_parse_oca_dependencies(self):
        oca_dependencies_should_be = [['addons-vauxoo',
                                       'https://github.com/Vauxoo/addons-vauxoo.git',
                                       '8.0']]
        self.assertListEqual(self.odoo_afr.oca_dependencies,
                             oca_dependencies_should_be)

    def test_05_modules_reference_bundle_instances(self):
        for module in self.odoo_afr.modules:
            self.assertIsInstance(module.bundle, Bundle)
            self.assertEqual(module.bundle.name, 'odoo-afr')

    def test_06_parse_complicated_oca_dependencies(self):
        oca_dependencies_should_be = [['addon', 'http://myurl.com/foo', 'branch'],
                                      ['foo', 'https://github.com/OCA/foo', '8.0'],
                                      ['bar', 'http://bar.foo/jhon', '8.0'],
                                      ['bundle', 'http://doe.com/joe', 'master'],
                                      ['odoo', 'http://another.url/', 'anotherbranch']]
        self.assertListEqual(self.oca_deps.oca_dependencies,
                             oca_dependencies_should_be)


class TestBrokenBundle(unittest.TestCase):

    def setUp(self):
        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.exampledir = os.path.join(self.testdir, 'examples')
        self.broken_manifest_dir = os.path.join(self.exampledir, 'broken-manifest')
        self.is_not_package_dir = os.path.join(self.exampledir, 'is-not-package')
        self.non_existent_dir = os.path.join(self.exampledir, 'non-existent')
        self.empty_dir = os.path.join(self.exampledir, 'empty')

    def test_01_non_existent_bundle(self):
        self.assertRaisesRegexp(
            AssertionError, '%s is not a directory or does not exist.' % self.non_existent_dir,
            Bundle, self.non_existent_dir, exclude_tests=False
        )

    def test_02_empty_bundle(self):
        self.assertRaisesRegexp(
            AssertionError, 'The specified path does not contain valid Odoo modules.',
            Bundle, self.empty_dir, exclude_tests=False
        )

    def test_03_broken_manifest(self):
        self.assertRaisesRegexp(
            IOError, 'An error ocurred while reading.*',
            Bundle, self.broken_manifest_dir, exclude_tests=False
        )

    def test_04_is_not_package(self):
        self.assertRaisesRegexp(
            AssertionError, 'The module is not a python package.',
            Bundle, self.is_not_package_dir, exclude_tests=False
        )

def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite('pipsalabim.bundle'))
    return tests

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
