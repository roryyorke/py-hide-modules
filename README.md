This is utility to temporarily make a module hidden from import; the
motivating application is to have test coverage of the catch-block in:

````python
def frobnicate(spork):
  try:
    import non_standard_module
  catch ImportError:
    raise MyError('You need non_standard_module to frobnicate a spork')
````

You can use the hide_modules.hide_modules decorator on a simple test
for ImportError:

````python
class TestFrobnicator(object):
  @hide_modules(['non_standard_module']):
  def testNoNonStandardModule(self):
    self.assertRaises(ImportError,frobnicate,spork)
````

Passes tests on Python 2.7, Python 3.4, and PyPy 2.7 on Ubuntu 14.04,
and Python 2.7, 3.2, 3.3, 3.4, PyPy, and PyPy3 on Travis CI.

Don't use this on core modules like "sys".

If your handling of a missing module is simple (as in the example
above), you may be better off just marking the line as being excluded
from testing, e.g., https://coverage.readthedocs.org/en/coverage-4.0a5/excluding.html

[![Build Status](https://travis-ci.org/roryyorke/py-hide-modules.svg?branch=master)](https://travis-ci.org/roryyorke/py-hide-modules)
