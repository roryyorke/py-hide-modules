# Demonstrate use of hide_modules

# code from here to "import unittest" represents a module under test

# our own error class; we're going to turn ImportErrors into one of these
class MyError(RuntimeError):
  pass

# a function that handles ImportErrors
def frobnicate(spork):
  try:
    import non_standard_module
  except ImportError:
    # in this case "handle" is just "translate to our own class of
    # exception", which is barely worth testing
    raise MyError('You need non_standard_module to frobnicate a spork')

# here starts the test code
import unittest
import hide_modules

class TestFrobnicator(unittest.TestCase):
  # the module will be hidden for this test only
  @hide_modules.hide_modules(['non_standard_module'])
  def testNoNonStandardModule(self):
    """test that we get expected error when non_standard_module isn't present"""
    spork = 1.234
    self.assertRaises(MyError,frobnicate,spork)

if __name__ == '__main__':
    unittest.main()
