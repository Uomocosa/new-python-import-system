# This is the __init__.py that get's called when you import this package!
import sys
import os
import inspect
import warnings
import importlib.util
import importlib.abc
from types import ModuleType
from pathlib import Path

def P(path) -> Path: return Path(path).absolute()

DEBUG = True
VERBOSE = False

THIS_FILE_PATH = P(__file__)
if DEBUG: print(f">>> THIS_FILE_PATH: {THIS_FILE_PATH}")


class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder's find_spec")
        if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if path is None: return None
        assert len(path) == 1, "Did not account for multiple paths, create a test for this, and solve it!"
        path = P(path[0])
        parts = fullname.split('.')
        possible_modules = ['.'.join(parts[:i]) for i in range(1, len(parts) + 1)]
        if DEBUG: print(f">>> possible_modules: {possible_modules}")
        packages_to_import = [path / m / "__init__.py" for m in possible_modules]
        packages_to_import = [d for d in packages_to_import if d.exists()]
        modules_to_import = [path / f"{m}.py" for m in possible_modules]
        modules_to_import = [f for f in modules_to_import if f.exists()]
        if len(packages_to_import) + len(modules_to_import) > 1:
            wrn_msg = f"\n>>> Found multiple packages/modules that could be imported: "
            if packages_to_import: wrn_msg += f"\n>>> packages:{packages_to_import}"
            if modules_to_import: wrn_msg += f"\n>>> modules:{modules_to_import}"
            wrn_msg += f"\n>>> I will import only the first one found."
            warnings.warn(wrn_msg)
        if DEBUG: print(f">>> packages_to_import: {packages_to_import}")
        if DEBUG: print(f">>> modules_to_import: {modules_to_import}")
        if packages_to_import:
            package_to_import = packages_to_import[0]
            original_loader = importlib.machinery.SourceFileLoader(fullname, str(package_to_import))
            spec = importlib.util.spec_from_file_location(
                fullname,
                package_to_import,
                submodule_search_locations=[str(path)],
                loader=CallableLoader(original_loader),
            )
        elif modules_to_import:
            file_to_import = modules_to_import[0]
            original_loader = importlib.machinery.SourceFileLoader(fullname, str(package_to_import))
            spec = importlib.util.spec_from_file_location(
                fullname,
                file_to_import,
                submodule_search_locations=None,
                loader=CallableLoader(original_loader),
            )
        else: return None
        return spec


class CallableLoader(importlib.abc.Loader):
    def __init__(self, original_loader):
        self.original_loader = original_loader

    def create_module(self, spec):
        # Let the original loader create the module object
        # This is often just 'None', letting importlib handle it.
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        """
        This is the most important method.
        """
        try:
            # THIS IS THE FIX:
            # Tell the original loader to run the .py file's code.
            # This will populate 'module.__dict__' with 'fun1', 'var1', etc.
            self.original_loader.exec_module(module)

            # Now you can run your own custom logic AFTER
            # the module is loaded.
            # print(f">>> CallableLoader finished executing {module.__name__}")
            # ... your custom code ...

        except Exception as e:
            print(f"Error during exec_module for {module.__name__}: {e}")
            raise



# Works fine, but is a little hacky
# def get_importer_filepath() -> Path:
#     """
#     Walks the stack to find the first frame that 
#     is NOT part of the importlib machinery.
#     """
#     import_frames = inspect.stack()
#     import_frames = [x for x in import_frames if not x.filename.startswith("<frozen importlib")]
#     import_frames = [x for x in import_frames if not Path(x.filename) == THIS_FILE_PATH]
#     if DEBUG and VERBOSE: [print(frame.filename) for frame in import_frames]
#     if not import_frames: return None
#     return P(import_frames[0].filename)




def install_hook():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">>> new_import_system's hook installed")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())

install_hook()