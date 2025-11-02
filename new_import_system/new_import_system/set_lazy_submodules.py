import pkgutil
from types import ModuleType
from .P import P
from .LazyModule import LazyModule

def set_lazy_submodules(module: ModuleType, DEBUG=False):
    if DEBUG: print(f">F> set_lazy_submodules")
    for _, name, ispkg in pkgutil.iter_modules(module.__path__):
        if name.startswith('_'): continue # Optional: ignore private modules
        full_import_name = f"{module.__name__}.{name}"
        if DEBUG: print(f">>> module.__file__: {module.__file__}")
        submodule_path = P(module.__file__).parent / name
        if DEBUG: print(f">>> submodule_path: {submodule_path}")
        setattr(module, name, LazyModule(full_import_name, submodule_path))
    return module

# def set_lazy_submodules(module: ModuleType, DEBUG=False):
#     if DEBUG: print(f">F> set_lazy_submodules")
#     lazy_submodules = {}
#     for _, name, _ in pkgutil.iter_modules(module.__path__):
#         if name.startswith('_'): continue # Optional: ignore private modules
#         full_import_name = f"{module.__name__}.{name}"
#         lazy_submodules[name] = full_import_name
#     setattr(module, '__lazy_submodules__', lazy_submodules)
#     [setattr(module, )]
#     if DEBUG: print(f">>> lazy_submodules: {lazy_submodules}")
#     return module