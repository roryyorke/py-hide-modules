"""Hide modules from import

 ModuleHider - import finder hook and context manager
 hide_modules - decorator using ModuleHider
"""

try:
    import importlib.abc
    # py>=3.3 has MetaPathFinder
    _ModuleHiderBase = getattr(importlib.abc, 'MetaPathFinder',
                               importlib.abc.Finder)
except ImportError:
    # py2
    _ModuleHiderBase = object


class ModuleHider(_ModuleHiderBase):
    """Import finder hook to hide specified modules
    ModuleHider(hidden_modules) -> instance
    hidden_modules is a list of strings naming modules to hide.
    """

    def __init__(self, hidden):
        self.hidden = hidden

    # python <=3.3
    def find_module(self, fullname, path=None):
        return self.find_spec(fullname, path)

    # python >=3.4
    def find_spec(self, fullname, path, target=None):
        if fullname in self.hidden:
            raise ImportError('No module named {}'.format(fullname))

    def hide(self):
        "Starting hiding modules"
        import sys
        if self in sys.meta_path:
            raise RuntimeError("Already hiding modules")
        # must be first to override standard finders
        sys.meta_path.insert(0, self)
        # remove hidden modules to force reload
        for m in self.hidden:
            if m in sys.modules:
                del sys.modules[m]

    def unhide(self):
        "Unhide modules"
        import sys
        sys.meta_path.remove(self)

    def __enter__(self):
        self.hide()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unhide()

    # there's much point in __del__: sys.meta_path will keep a
    # reference to an object on which .unhide() is not called, so
    # refcount will only go to 0 if the object is removed from
    # sys.meta_path somehow (in which case deletion doesn't
    # matter), or when Python exits (ditto)


def hide_modules(hidden):
    """hide_modules(hidden_modules) -> decorator

    When decorated function is called, the specified list of modules
    will be hidden; once the function exits, the modules will be
    unhidden.
    """
    def applydec(f):
        def decf(*args, **kwargs):
            with ModuleHider(hidden):
                f(*args, **kwargs)
        # carry across name so that nose still finds the test
        decf.__name__ = f.__name__
        # and carry across doc for test descriptions (etc.)
        decf.__doc__ = f.__doc__
        return decf
    return applydec
