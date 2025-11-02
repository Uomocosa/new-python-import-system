from types import ModuleType

def set_call_wrapper(module: ModuleType, DEBUG=False):
    if DEBUG: print(f">F> set_call_wrapper")
    if DEBUG: print(f">>> module.__name__: {module.__name__}")
    original_call_fn = getattr(module, '__call__', None)
    def __call__(*args, **kwargs):
        if DEBUG: print(f">F> __call__")
        if hasattr(module, '__call__'): 
            return module.__call__(*args, **kwargs)
        if hasattr(module, module.__name__): 
            call_fn = getattr(module, module.__name__)
            return call_fn(*args, **kwargs)
        if original_call_fn:
            return original_call_fn(*args, **kwargs)
        else:
            err_msg  = f"module '{module.__name__}' not callable"
            err_msg += f"\n You can call it if you add a function '__call__' in it."
            err_msg += f"\n Or a function with the same name ('{module.__name__}')"
            raise TypeError(err_msg)
    setattr(module, '__call__', __call__)
    return module