# This is the __init__.py that get's called when you import this package!
import sys
import warnings
import importlib
import importlib.util
import importlib.abc
from pathlib import Path
from .P import P
from .timeit import timeit
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
TIMEIT = False

class CallableFinder(importlib.abc.MetaPathFinder):
    def __init__(self, top_level_package_dir: Path):
        if DEBUG: print(f"CallableFinder.__init__(top_level_package_dir: {top_level_package_dir})")
        self.top_level_package_dir = P(top_level_package_dir)
        self.top_level_name = P(top_level_package_dir).name
        
    # @timeit # COMMENT THIS!
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder find_spec")
        # if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        # print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if fullname == '__init__' and not path and not target: return None
        if not fullname.startswith(self.top_level_name): return None
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
            if DEBUG: print(f">>> possible_imports: {possible_imports}")
            possible_imports = [x for x in possible_imports if x.exists()]
            if DEBUG: print(f">>> possible_imports: {possible_imports}")
            if DEBUG: print(f">>> self.top_level_package_dir: {self.top_level_package_dir}")
            possible_imports = [x for x in possible_imports if P(x).is_relative_to(P(self.top_level_package_dir))]
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



def install(top_level_package_init):
    """Prepends our custom finder to the meta_path."""
    top_level_package_init = P(top_level_package_init)
    assert top_level_package_init.exists()
    assert top_level_package_init.name == "__init__.py", "install function must be called inside the top-level __init__.py file of your project"

    if DEBUG: print(f">F> install(top_level_package_init: {top_level_package_init})")
    top_level_package_dir = top_level_package_init.parent
    callable_finder_isntances = [i for i in sys.meta_path if isinstance(i, CallableFinder)]
    callable_finder_isntances = [i for i in callable_finder_isntances if i.top_level_package_dir == top_level_package_dir]
    if not any(callable_finder_isntances):
        sys.meta_path.insert(0, CallableFinder(top_level_package_dir))

    sys_key = top_level_package_dir.name
    if DEBUG: print(f"sys_key: {sys_key}")
    if not sys_key in sys.modules: return
    sys.modules[sys_key] = set_lazy_submodules(sys.modules[sys_key])
    sys.modules[sys_key] = make_module_callable(sys.modules[sys_key])
    if not '__main__' in sys.modules: return
    main_script = sys.modules['__main__']
    if DEBUG: print(f"main_script: {main_script}")
    if not hasattr(main_script, '__file__'): return
    if DEBUG: print(f"P(main_script.__file__): {P(main_script.__file__)}")
    if DEBUG: print(f"P(top_level_package_dir): {P(top_level_package_dir)}")
    if not P(main_script.__file__).is_relative_to(P(top_level_package_dir.parent)): return
    relative_path = P(main_script.__file__).relative_to(P(top_level_package_dir.parent))
    if DEBUG: print(f"relative_path: {relative_path}")
    if DEBUG: print(f"relative_path: {relative_path}")
    main_script.__package__ = '.'.join(relative_path.parent.parts)
    if DEBUG: print(f"main_script.__package__: {main_script.__package__}")
