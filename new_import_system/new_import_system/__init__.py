# This is the __init__.py that get's called when you import this package!
import sys
import warnings
import importlib
import importlib.util
import importlib.abc
from .P import P
from .get_importers_stack import get_importers_stack
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



def install():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">F> install()")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())
    
    importers = get_importers_stack()
    top_package_init = importers[1]
    assert top_package_init.name == "__init__.py", "Install new_importer_system inside the '__init__.py' of your top level package of your project"
    if DEBUG: print(f"top_package_init: {top_package_init}")
    top_package = top_package_init.parent
    sys_key = top_package.name
    if DEBUG: print(f"sys_key: {sys_key}")
    if not sys_key in sys.modules: return
    sys.modules[sys_key] = set_lazy_submodules(sys.modules[sys_key])
    sys.modules[sys_key] = make_module_callable(sys.modules[sys_key])
    if not '__main__' in sys.modules: return
    main_script = sys.modules['__main__']
    if DEBUG: print(f"main_script: {main_script}")
    if not hasattr(main_script, '__file__'): return
    if DEBUG: print(f"P(main_script.__file__): {P(main_script.__file__)}")
    if DEBUG: print(f"P(top_package): {P(top_package)}")
    if not P(main_script.__file__).is_relative_to(P(top_package.parent)): return
    relative_path = P(main_script.__file__).relative_to(P(top_package.parent))
    if DEBUG: print(f"relative_path: {relative_path}")
    if DEBUG: print(f"relative_path: {relative_path}")
    main_script.__package__ = '.'.join(relative_path.parent.parts)
    if DEBUG: print(f"main_script.__package__: {main_script.__package__}")
    