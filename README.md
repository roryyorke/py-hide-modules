[![Build Status](https://travis-ci.org/roryyorke/py-hide-modules.svg?branch=master)](https://travis-ci.org/roryyorke/py-hide-modules)

Introduction
============

This is a utility to temporarily make a module hidden from import; the
motivating application is to have test coverage of the except clause
in code like this:

````python
# a function that handles ImportErrors
def frobnicate(spork):
  try:
    import non_standard_module
  except ImportError:
    # in this case "handle" is just "translate to our own class of
    # exception", which is barely worth testing
    raise MyError('You need non_standard_module to frobnicate a spork')
````

You can use the `hide_modules.hide_modules` decorator on a simple test
for ImportError:

````python
class TestFrobnicator(unittest.TestCase):
  # the module will be hidden for this test only
  @hide_modules.hide_modules(['non_standard_module'])
  def testNoNonStandardModule(self):
    spork = 1.234
    self.assertRaises(MyError,frobnicate,spork)
````

The specified list of modules will only be hidden for the duration of
the test.

The decorator preserves the function name and docstring.

See `example.py` in this repository for a complete example of the
above, and look at `test_hide_modules.py` for a comprehensive
demonstration of what `hide_modules` can do.

The decorator works well if the ```try-import-except ImportError```
statement is in a function body.  You can use the
`hide_modules.ModuleHider` class for more general control of when
hiding starts and stops.  In case it isn't obvious, the hiding must
start *before* the relevant import statement is executed!

Passes tests on Python 2.7, Python 3.4, and PyPy 2.7 on Ubuntu 14.04,
and Python 2.7, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, PyPy, and PyPy3 on Travis CI.

Don't use this on core modules like `sys`.

If the handling of a missing module is simple, as in the example
above, you may be better off just marking the line as being excluded
from testing, e.g., https://coverage.readthedocs.org/en/coverage-4.0a5/excluding.html

Installation
============

Copy `hide_modules.py` to your test directory.

Limitations
===========

You should only use this in test code, and only to test `ImportError`
branches.

Ideally, you would run all tests that rely on a particular module
being hidden _before_ that module is _ever_ imported. `hide_modules`
will probably work anyway: if an already-imported module is hidden, it
is temporarily removed from `sys.modules`, and this may be sufficient
for many or even most cases.  However, side-effects that occur due to
a module being imported _cannot_ be hidden or undone; such a
side-effect might be the imported module monkey-patching another.
