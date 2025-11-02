# This is the __init__.py that get's called when you import this package!
import sys
import os
import inspect
import warnings
import pkgutil
import importlib
import importlib.util
import importlib.abc
from types import ModuleType
from pathlib import Path
from .get_importer_filepath import get_importer_filepath
from .set_call_wrapper import set_call_wrapper
from .set_dir_wrapper import set_dir_wrapper
from .set_getattr_wrapper import set_getattr_wrapper
from .set_lazy_submodules import set_lazy_submodules
from .P import P


DEBUG = False
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
        if not path: return
        assert len(path) == 1, "Did not account for multiple paths, create a test for this, and solve it!"
        search_path = P(path[0])
        parts = fullname.split('.')
        possible_modules = ['.'.join(parts[:i]) for i in range(1, len(parts) + 1)]
        if DEBUG: print(f">>> possible_modules: {possible_modules}")
        package_init_file = search_path / parts[-1] / "__init__.py"
        modules_to_import = [search_path / f"{m}.py" for m in possible_modules]
        modules_to_import = [f for f in modules_to_import if f.exists()]
        if package_init_file.exists() + len(modules_to_import) > 1:
            wrn_msg = f"\n>>> Found multiple packages/modules that could be imported: "
            if package_init_file: wrn_msg += f"\n>>> package:{package_init_file}"
            if modules_to_import: wrn_msg += f"\n>>> modules:{modules_to_import}"
            wrn_msg += f"\n>>> I will import only the first one found."
            warnings.warn(wrn_msg)
        if DEBUG: print(f">>> package_init_file: {package_init_file}")
        if DEBUG: print(f">>> modules_to_import: {modules_to_import}")
        if package_init_file.exists():
            if DEBUG: print(f">>> IMPORTING PACKAGE: '{package_init_file}'")
            original_loader = importlib.machinery.SourceFileLoader(fullname, str(package_init_file))
            spec = importlib.util.spec_from_file_location(
                fullname,
                package_init_file,
                submodule_search_locations=[str(package_init_file.parent)],
                loader=CallableLoader(original_loader),
            )
        elif modules_to_import:
            module_to_import = modules_to_import[0]
            if DEBUG: print(f">>> IMPORTING MODULE: '{module_to_import}'")
            original_loader = importlib.machinery.SourceFileLoader(fullname, str(package_init_file))
            spec = importlib.util.spec_from_file_location(
                fullname,
                module_to_import,
                submodule_search_locations=None,
                loader=CallableLoader(original_loader),
            )
        else: return
        return spec



class CallableLoader(importlib.abc.Loader):
    def __init__(self, original_loader):
        self.original_loader = original_loader

    def create_module(self, spec):
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        self.original_loader.exec_module(module)
        if not hasattr(module, '__path__'): return
        if DEBUG: print(f">>> Auto-scanning and attaching submodules for: {module.__name__}")
        module = set_lazy_submodules(module, DEBUG=True)

def install_hook():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">>> new_import_system's hook installed")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())



install_hook()