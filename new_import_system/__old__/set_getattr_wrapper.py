import importlib
from types import ModuleType
from .LazyModule import LazyModule

def set_getattr_wrapper(module: ModuleType, DEBUG=False):
    if DEBUG: print(f">F> set_getattr_wrapper")
    if DEBUG: print(f">>> module.__name__: {module.__name__}")
    original_getattr_fn = getattr(module, '__getattr__', None)
    def __getattr__(name: str):
        if DEBUG: print(f">F> __getattr__('{name}')")
        if DEBUG: print(f">>> [LazyLoader] __getattr__ triggered for '{name}' on '{module.__name__}'")
        if not hasattr(module, '__lazy_submodules__'): 
            if original_getattr_fn: original_getattr_fn(name)
            else: return
        if name not in module.__lazy_submodules__: 
            if original_getattr_fn: original_getattr_fn(name)
            else: return
        full_import_name = module.__lazy_submodules__.get(name)
        if DEBUG: print(f">>> [LazyLoader] Lazily importing: {full_import_name}")
        sub_module = importlib.import_module(full_import_name)
        setattr(module, name, sub_module)
        return sub_module
    setattr(module, '__getattr__', __getattr__)
    return module