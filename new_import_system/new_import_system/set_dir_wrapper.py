from types import ModuleType

def set_dir_wrapper(module: ModuleType, DEBUG=False):
    if DEBUG: print(f">F> set_dir_wrapper")
    original_dir_fn = module.__dir__
    def __dir__():  
        if DEBUG: print(f">F> __dir__")
        attributes = original_dir_fn()
        if not hasattr(module, '__lazy_submodules__'): return sorted(list(attributes))
        [attributes.add(k) for k in module.__lazy_submodules__.keys()]
        return sorted(list(attributes))
    setattr(module, '__dir__', __dir__)
    return module