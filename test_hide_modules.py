#!/usr/bin/env python

import unittest

import hide_modules


def import_csv():
    import csv


def import_wsgiref_handlers():
    import wsgiref.handlers


@hide_modules.hide_modules(['csv', 'wsgiref.handlers'])
def blocked_import_csv():
    import_csv()


@hide_modules.hide_modules(['csv', 'wsgiref.handlers'])
def blocked_import_wsgiref_handlers():
    import_wsgiref_handlers()


class TestHideModules(unittest.TestCase):

    def testHideUnhide(self):
        "Test ModuleHider hide and unhide methods"
        mh = hide_modules.ModuleHider(['csv', 'wsgiref.handlers'])
        import_csv()
        import_wsgiref_handlers()
        mh.hide()
        self.assertRaises(ImportError, import_csv)
        self.assertRaises(ImportError, import_wsgiref_handlers)
        mh.unhide()
        import_csv()
        import_wsgiref_handlers()

    def testContextManager(self):
        "Test ModuleHider as context manager"
        import_csv()
        import_wsgiref_handlers()
        with hide_modules.ModuleHider(['csv', 'wsgiref.handlers']):
            self.assertRaises(ImportError, import_csv)
            self.assertRaises(ImportError, import_wsgiref_handlers)
        import_csv()
        import_wsgiref_handlers()

    def testDecorator(self):
        "Test hide_modules decorator"
        import_csv()
        import_wsgiref_handlers()
        self.assertRaises(ImportError, blocked_import_csv)
        self.assertRaises(ImportError, blocked_import_wsgiref_handlers)
        import_csv()
        import_wsgiref_handlers()

    @hide_modules.hide_modules(['csv', 'wsgiref.handlers'])
    def testDecoratorOnTest(self):
        "Test hide_modules applied to test method"
        self.assertRaises(ImportError, import_csv)
        self.assertRaises(ImportError, import_wsgiref_handlers)

    def testRestoringHiddenModules(self):
        """Test that unhidden modules are restored.

        Some packages---e.g., encodings from stdlib, and numpy---must
        be restored to sys.modules, or they cannot be re-imported.

        This is a regression test; modules were previously *not*
        restored, which caused problems in Python 2.
        """
        def fallback_on_import():
            try:
                import encodings
                self.assertTrue(False)
            except ImportError:
                pass

        @hide_modules.hide_modules(['encodings'])
        def fn():
            fallback_on_import()

        import encodings
        fn()
        import encodings


if __name__ == '__main__':
    unittest.main()
