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

DEBUG = True
VERBOSE = False

class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder find_spec")
        # if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if fullname == '__init__' and not path and not target: return None
        name = fullname.split('.')[-1]
        if DEBUG: print(f">>> name: {name}")
        if path is None: 
            # This is a top-level import, like 'import package'. Search sys.path.
            if VERBOSE: print(f"sys.path: {sys.path}") 
            search_paths = [P(p) for p in sys.path if p and P(p).is_dir()]
        else:
            # This is a submodule import. like 'import package.subpackage' Search the parent's __path__.
            search_paths = [P(p) for p in path if p and P(p).is_dir()]
        if VERBOSE: print(f"search_paths: {search_paths}") 
        for search_path in search_paths:
            possible_imports = []
            possible_imports += [search_path / name / "__init__.py"]
            possible_imports += [search_path / f"{name}{stem}" for stem in IMPORTABLE_EXTENSIONS]
            possible_imports = [x for x in possible_imports if x.exists()]
            if DEBUG: print(f">>> possible_imports: {possible_imports}")
            if len(possible_imports) > 1:
                wrn_msg = f"\n>>> Found multiple packages/modules that could be imported: "
                wrn_msg += f"\n>>> packages/modules:{possible_imports}"
                wrn_msg += f"\n>>> I will import only the first one found."
                warnings.warn(wrn_msg)
            if not possible_imports: return None
            to_import = possible_imports[0]
            if to_import.name == '__init__.py':
                if DEBUG: print(f">>> IMPORTING PACKAGE: '{to_import}'")
                # fullname = to_import.parent.name
                submodule_search_locations = [str(to_import.parent)]
            else:
                if DEBUG: print(f">>> IMPORTING MODULE: '{to_import}'")
                submodule_search_locations = None
            original_loader = importlib.machinery.SourceFileLoader(
                fullname, 
                str(to_import),
            )
            spec = importlib.util.spec_from_file_location(
                fullname,
                to_import,
                submodule_search_locations=submodule_search_locations,
                loader=CallableLoader(original_loader),
            )
            return spec



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