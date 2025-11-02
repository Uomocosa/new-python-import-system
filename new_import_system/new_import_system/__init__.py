# This is the __init__.py that get's called when you import this package!
import sys
import warnings
import importlib
import importlib.util
import importlib.abc
from .P import P
from .get_importer_filepath import get_importer_filepath
from .set_lazy_submodules import set_lazy_submodules
from .make_module_callable import make_module_callable

IMPORTABLE_EXTENSIONS = [
    ".py",
    ".pyc", 
    ".pyd",
    ".so",
]

DEBUG = False
VERBOSE = False

# THIS_FILE_PATH = P(__file__)
# if DEBUG: print(f">>> THIS_FILE_PATH: {THIS_FILE_PATH}")


class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder find_spec")
        # if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if path is None: 
            # This is a top-level import, like 'import package'. Search sys.path.
            search_paths = [P(p) for p in sys.path if p and P(p).is_dir()]
        else:
            # This is a submodule import. like 'import package.subpackage' Search the parent's __path__.
            search_paths = [P(p) for p in path if p and P(p).is_dir()]
        name = fullname.split('.')[-1]
        for search_path in search_paths:
            package_init_file = search_path / name / "__init__.py"
            modules_to_import = [search_path / f"{name}{stem}" for stem in IMPORTABLE_EXTENSIONS]
            modules_to_import = [f for f in modules_to_import if f.exists()]
            if DEBUG: print(f">>> package_init_file: {package_init_file}")
            if DEBUG: print(f">>> modules_to_import: {modules_to_import}")
            if package_init_file.exists() + len(modules_to_import) > 1:
                wrn_msg = f"\n>>> Found multiple packages/modules that could be imported: "
                if package_init_file: wrn_msg += f"\n>>> package:{package_init_file}"
                if modules_to_import: wrn_msg += f"\n>>> modules:{modules_to_import}"
                wrn_msg += f"\n>>> I will import only the first one found."
                warnings.warn(wrn_msg)
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
                original_loader = importlib.machinery.SourceFileLoader(fullname, str(module_to_import))
                spec = importlib.util.spec_from_file_location(
                    fullname,
                    module_to_import,
                    submodule_search_locations=None,
                    loader=CallableLoader(original_loader),
                )
            else: return
            return spec
        if DEBUG: "module '{fullname}' was not found"



class CallableLoader(importlib.abc.Loader):
    def __init__(self, original_loader):
        self.original_loader = original_loader

    def create_module(self, spec):
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        self.original_loader.exec_module(module)
        if hasattr(module, '__path__'): 
            if DEBUG: print(f">>> Auto-scanning and attaching submodules for: {module.__name__}")
            module = set_lazy_submodules(module, DEBUG=False)
        module = make_module_callable(module, DEBUG=False, VERBOSE=False)



def install_hook():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">>> new_import_system's hook installed")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())



install_hook()