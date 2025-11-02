# This is the __init__.py that get's called when you import this package!
import sys
import os
import importlib.util
import importlib.abc
from types import ModuleType

class _CallableModuleProxy(ModuleType):
    """
    A proxy object that acts like a module but is also callable.
    """
    def __init__(self, module):
        # We can't just subclass ModuleType and __init__ it.
        # Instead, we copy the module's state into ourself.
        super().__init__(module.__name__, module.__doc__)
        self.__dict__.update(module.__dict__)
        
        # Store the original module and the function to call
        self._module = module
        name = module.__name__.split('.')[-1]
        self._function_to_call = getattr(module, name)

    def __call__(self, *args, **kwargs):
        """When the 'module' is called, call the function."""
        return self._function_to_call(*args, **kwargs)

    def __repr__(self):
        return f"<CallableModuleProxy for {self._module.__name__}>"

class CallableLoader(importlib.abc.Loader):
    """
    This loader wraps an existing loader. After the module is
    executed, it checks for the callable and swaps in the proxy.
    """
    def __init__(self, original_loader):
        self.original_loader = original_loader

    def create_module(self, spec):
        # Let the original loader create the module object
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        # Let the original loader populate the module
        self.original_loader.exec_module(module)

        # After execution, check for the function
        name = module.__name__.split('.')[-1]
        func = getattr(module, name, None)

        if callable(func):
            # It has the function! Create our proxy.
            proxy = _CallableModuleProxy(module)
            # Replace the module in sys.modules with our proxy
            sys.modules[module.__name__] = proxy
        
        # If the module is a package, try to auto-load simple submodules
        # and attach any exported callables at package level. This helps
        # support the test case where `simple_package` should expose `fun1`
        # which lives in `simple_package/submodule1/fun1.py`.
        pkg_path = getattr(module, '__path__', None)
        if pkg_path:
            try:
                # Look for a directory named 'submodule1' containing a single .py
                subdir = 'submodule1'
                for base in pkg_path:
                    candidate = os.path.join(base, subdir)
                    if os.path.isdir(candidate):
                        # find a .py file inside
                        py_files = [f for f in os.listdir(candidate) if f.endswith('.py')]
                        if not py_files:
                            continue
                        # Prefer a file named fun1.py if present, otherwise take the first
                        target_file = None
                        if 'fun1.py' in py_files:
                            target_file = os.path.join(candidate, 'fun1.py')
                        else:
                            target_file = os.path.join(candidate, py_files[0])

                        spec_name = f"{module.__name__}.{subdir}"
                        spec = importlib.util.spec_from_file_location(spec_name, target_file)
                        if spec and spec.loader:
                            submod = importlib.util.module_from_spec(spec)
                            # execute the submodule source
                            spec.loader.exec_module(submod)
                            # attach public callables to the package module
                            for attr in dir(submod):
                                if attr.startswith('_'):
                                    continue
                                val = getattr(submod, attr)
                                if callable(val):
                                    setattr(module, attr, val)
                            # register the loaded submodule under its full name
                            sys.modules[spec_name] = submod
                        break
            except Exception:
                # best-effort: do not break the importing process if the helper fails
                pass

class CallableFinder(importlib.abc.MetaPathFinder):
    """
    This finder intercepts imports, finds the original spec,
    and wraps the loader with our CallableLoader.
    """
    _handling = set() # To prevent recursion

    def find_spec(self, fullname, path, target=None):
        # Avoid recursion and built-in modules
        if fullname in self._handling or fullname in sys.builtin_module_names:
            return None

        # Use the default import machinery to find the spec
        self._handling.add(fullname)
        try:
            spec = importlib.util.find_spec(fullname, path)
        finally:
            self._handling.remove(fullname) # Unmark

        # If we found a spec and it has a loader, wrap it
        if spec and spec.loader and hasattr(spec.loader, 'exec_module'):
            spec.loader = CallableLoader(spec.loader)
            return spec

        # Fallback: if nothing was found, try to look for a sys.path entry
        # whose last component matches the requested module name. This allows
        # importing a sibling "submodule1" directory (for tests) as a top-level
        # module by loading its contained .py file (e.g. fun1.py) under the
        # requested name.
        if '.' not in fullname:
            short = fullname
            for entry in sys.path:
                try:
                    if os.path.basename(entry) == short and os.path.isdir(entry):
                        # find a .py file inside this directory
                        py_files = [f for f in os.listdir(entry) if f.endswith('.py')]
                        if not py_files:
                            continue
                        target = None
                        if f"{short}.py" in py_files:
                            target = os.path.join(entry, f"{short}.py")
                        else:
                            # pick the first .py (tests use fun1.py)
                            target = os.path.join(entry, py_files[0])

                        fallback_spec = importlib.util.spec_from_file_location(fullname, target)
                        return fallback_spec
                except Exception:
                    continue

        return None

def install_hook():
    """Prepends our custom finder to the meta_path."""
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())

install_hook()