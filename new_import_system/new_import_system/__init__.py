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

# top_level_package = Path('.').absolute()
# print(f">>> top_level_package: {top_level_package}")

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
        if DEBUG: print(f"module: {module}")
        if DEBUG: print(f"dir(module): {dir(module)}")
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
        if DEBUG: print(f">F> CallableLoader's __init__")
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

        # Start by assuming the module we attach to is the original
        module_to_attach_to = module 

        if callable(func):
            if DEBUG: print(f">>> Found callable {name} in {module.__name__}. Creating proxy.")
            # It has the function! Create our proxy.
            proxy = _CallableModuleProxy(module)
            # Replace the module in sys.modules with our proxy
            sys.modules[module.__name__] = proxy
            # Any new attributes must be attached to the proxy, not the old module
            module_to_attach_to = proxy
        
        # --- Part 2: Auto-load .py files from package dir ---
        pkg_path = getattr(module, '__path__', None)
        if pkg_path:
            try:
                for base in pkg_path: # e.g., '.../submodule1'
                    if not os.path.isdir(base):
                        continue

                    # Find all .py files except __init__.py
                    py_files = [f for f in os.listdir(base) if f.endswith('.py') and not f == '__init__.py']
                    if DEBUG: print(f">>> Found .py files in {base}: {py_files}")
                    
                    for py_file in py_files:
                        sub_module_name = py_file[:-3] # e.g., 'fun1'
                        target_file = os.path.join(base, py_file)

                        # e.g., 'submodule1.fun1'
                        spec_name = f"{module.__name__}.{sub_module_name}"
                        
                        # Avoid re-importing if it's already there
                        if spec_name in sys.modules:
                            continue

                        spec = importlib.util.spec_from_file_location(spec_name, target_file)
                        
                        if spec and spec.loader:
                            submod = importlib.util.module_from_spec(spec)
                            
                            # IMPORTANT: Use the *original* loader (spec.loader)
                            # not a new CallableLoader, or you'll get recursion.
                            spec.loader.exec_module(submod)
                            
                            # Register the new submodule
                            sys.modules[spec_name] = submod
                            if DEBUG: print(f">>> Loaded submodule {spec_name}")

                            # Attach its public callables to the parent package
                            for attr_name in dir(submod):
                                if not attr_name.startswith('_'):
                                    val = getattr(submod, attr_name)
                                    if callable(val):
                                        if DEBUG: print(f">>> Attaching {spec_name}.{attr_name} to {module_to_attach_to.__name__} as {attr_name}")
                                        # Attach to the proxy or the original module
                                        setattr(module_to_attach_to, attr_name, val)
                                        
            except Exception as e:
                if DEBUG: print(f"Error during package auto-load: {e}")
                pass # best-effort



class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder's find_spec")
        if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if DEBUG: print(f">>> get_importer_filepath(): {get_importer_filepath()}")
        importer_file = get_importer_filepath()
        if path is None: # Top-level import (~ex.: 'import module1')
            if not importer_file: 
                if DEBUG: print(">>> No importer file, returning None")
                return None
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

        # CONTINUE FROM HERE!
        
        if DEBUG: print(f">>> importer_file: {importer_file}")
        if not importer_file: return None
        file_to_import = importer_file.parent / f"{fullname}.py"
        package_to_import = importer_file.parent / fullname / "__init__.py"
        if file_to_import.exists() and package_to_import.exists():
            warnings.warn(f"Found both a file and a python package named {fullname}, I will import the python package")
        if package_to_import.exists():
            if DEBUG: print(f">>> {fullname} is a package (dir)")
            spec = importlib.util.spec_from_file_location(
                fullname,
                package_to_import,
                submodule_search_locations=[str(importer_file.parent / fullname)] 
            )
        elif file_to_import.exists():
            if DEBUG: print(f">>> {fullname} is a file")
            spec = importlib.util.spec_from_file_location(
                fullname,
                file_to_import
            )
        else: return None
        if DEBUG: print(f">>> spec.loader: {spec.loader}")
        if spec.loader:
            if DEBUG: print(f">>> Wrapping loader for {fullname} with CallableLoader")
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