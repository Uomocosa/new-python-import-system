# This is the __init__.py that get's called when you import this package!
import sys
import os
import inspect
import warnings
import importlib.util
import importlib.abc
from types import ModuleType
from pathlib import Path

def P(path) -> Path: return Path(path).resolve()

DEBUG = True
VERBOSE = False

THIS_FILE_PATH = P(__file__)
if DEBUG: print(f">>> THIS_FILE_PATH: {THIS_FILE_PATH}")



class _CallableModuleProxy(ModuleType):
    """
    A proxy object that acts like a module but is also callable.
    It delegates all attribute access to the original module.
    """
    def __init__(self, module):
        # Initialize as a module type
        super().__init__(module.__name__, module.__doc__)
        
        # Use object.__setattr__ to set our internal attributes
        # to avoid triggering our own __setattr__ override.
        object.__setattr__(self, "_module", module)
        
        name = module.__name__.split('.')[-1]
        func = getattr(module, name, None)
        object.__setattr__(self, "_function_to_call", func)
        
        # Manually copy over special attributes that __getattr__
        # might not handle correctly for the import system.
        self.__file__ = getattr(module, '__file__', None)
        self.__loader__ = getattr(module, '__loader__', None)
        self.__package__ = getattr(module, '__package__', None)
        self.__spec__ = getattr(module, '__spec__', None)
        self.__path__ = getattr(module, '__path__', None)

    def __call__(self, *args, **kwargs):
        """When the 'module' is called, call the function."""
        if not callable(self._function_to_call):
             raise TypeError(f"Module {self.__name__} is not callable (function '{self._function_to_call}' not found or not callable)")
        return self._function_to_call(*args, **kwargs)

    def __repr__(self):
        return f"<CallableModuleProxy for {self._module.__name__} (callable: {callable(self._function_to_call)})>"

    def __getattr__(self, name):
        """Delegate attribute access to the original module."""
        try:
            return getattr(self._module, name)
        except AttributeError:
            # Raise a standard AttributeError
            raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Delegate attribute setting to the original module."""
        # Set our internal attributes directly
        if name in ("_module", "_function_to_call"):
            object.__setattr__(self, name, value)
        # Set all other attributes on the wrapped module
        else:
            setattr(self._module, name, value)
    
    def __delattr__(self, name):
        """Delegate attribute deletion to the original module."""
        delattr(self._module, name)

    def __dir__(self):
        """Delegate dir() to the original module."""
        return dir(self._module)
        
    @property
    def __dict__(self):
        """Delegate __dict__ access to the original module."""
        return self._module.__dict__


class CallableLoader(importlib.abc.Loader):
    """
    This loader wraps an existing loader. After the module is
    executed, it checks for the callable and swaps in the proxy.
    """
    def __init__(self, original_loader):
        if DEBUG: print(f">F> CallableLoader's __init__")
        if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> original_loader: {original_loader}")
        self.original_loader = original_loader

    def create_module(self, spec):
        # Let the original loader create the module object
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        # Let the original loader populate the module
        self.original_loader.exec_module(module)

        # --- Part 1: Make the module itself callable ---
        name = module.__name__.split('.')[-1]
        func = getattr(module, name, None)

        # Check if the module has a function with the same name and it's callable
        if func and callable(func):
            if DEBUG: print(f">>> Found callable '{name}' in module '{module.__name__}'. Creating proxy.")
            
            # Create the proxy
            proxy = _CallableModuleProxy(module)
            
            # CRITICAL Step 1: Replace the module in sys.modules with the proxy.
            # This handles 'import submodule1'
            sys.modules[module.__name__] = proxy
            
            # CRITICAL Step 2: Attach the proxy to the parent module.
            # This handles 'from package import submodule1'
            parts = module.__name__.split('.')
            if len(parts) > 1:
                parent_name = ".".join(parts[:-1])
                child_name = parts[-1]
                if parent_name in sys.modules:
                    parent_module = sys.modules[parent_name]
                    if DEBUG: print(f">>> Attaching proxy '{module.__name__}' to parent '{parent_name}' as '{child_name}'")
                    # Set the attribute on the parent module to be our *new proxy*
                    setattr(parent_module, child_name, proxy)
        
        # If no callable func is found, we do nothing.
        # The original module just stays in sys.modules as-is.



class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        # if DEBUG: print(f">F> CallableFinder's find_spec")
        # if DEBUG: print(f">>> self: {self}")
        # if DEBUG: print(f">>> fullname: {fullname}")
        # if DEBUG: print(f">>> path: {path}")
        # if DEBUG: print(f">>> target: {target}")
        # if DEBUG: print(f">>> get_importer_filepath(): {get_importer_filepath()}")
        importer_file = get_importer_filepath()
        if path is None: # Top-level import (~ex.: 'import module1')
            if not importer_file: return None
            search_dirs = [importer_file.parent]
            module_name_to_find = fullname # e.g., 'submodule1'
        else: # Submodule import (~ex.: 'from module1 import submodule1')
            search_dirs = path # e.g., ['.../package']
            module_name_to_find = fullname.split('.')[-1] # e.g., 'submodule1'
        base_dirs = [P(base_dir_str) for base_dir_str in search_dirs]
        files_to_import = [dir / f"{module_name_to_find}.py" for dir in base_dirs]
        packages_to_import = [dir / module_name_to_find / "__init__.py" for dir in base_dirs]
        files_to_import = [f for f in files_to_import if f.exists()]
        packages_to_import = [d for d in packages_to_import if d.exists()]
        assert len(files_to_import) <= 1, "How are there more than 1 FILE with the same name in this folder???"
        assert len(packages_to_import) <= 1, "How are there more than 1 PACKAGE with the same name in this folder???"
        if files_to_import and packages_to_import:
            warnings.warn(f"Found both a file and a python package named {fullname}, I will import the python package")
        if packages_to_import:
            package_to_import = packages_to_import[0]
            spec = importlib.util.spec_from_file_location(
                fullname,
                package_to_import,
                submodule_search_locations=[str(importer_file.parent / fullname)] 
            )
        elif files_to_import:
            file_to_import = files_to_import[0]
            spec = importlib.util.spec_from_file_location(
                fullname,
                file_to_import
            )
        else: return None
        # if DEBUG: print(f">>> spec.loader: {spec.loader}")
        if spec.loader:
            # if DEBUG: print(f">>> Wrapping loader for {fullname} with CallableLoader")
            spec.loader = CallableLoader(spec.loader)
        return spec



def get_importer_filepath() -> Path:
    """
    Walks the stack to find the first frame that 
    is NOT part of the importlib machinery.
    """
    import_frames = inspect.stack()
    import_frames = [x for x in import_frames if not x.filename.startswith("<frozen importlib")]
    import_frames = [x for x in import_frames if not Path(x.filename) == THIS_FILE_PATH]
    if DEBUG and VERBOSE: [print(frame.filename) for frame in import_frames]
    if not import_frames: return None
    return P(import_frames[0].filename)



def install_hook():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">>> new_import_system's hook installed")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())



install_hook()