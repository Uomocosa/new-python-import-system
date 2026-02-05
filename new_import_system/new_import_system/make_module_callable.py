import sys
import warnings
from types import ModuleType

DEBUG = False
VERBOSE = False

def make_module_callable(module, DEBUG=False, VERBOSE=False):
    # DEBUG = True
    if DEBUG: print(f">F> make_module_callable")
    if VERBOSE: print(f">>> dir(module): {dir(module)}")
    fn_name = module.__name__.split('.')[-1]
                    
    if DEBUG: print(f">>> fn_name: {fn_name}")
    if VERBOSE: print(f"module.__dict__.keys(): {module.__dict__.keys()}")
    if not any([x in module.__dict__ for x in ['__call__', fn_name]]): return module
    if all([x in module.__dict__ for x in ['__call__', fn_name]]): 
        wrn_msg  = f"Found both '__call__' and {fn_name} inside package/module '{module.__name__}'"
        wrn_msg += f"\n'__call__' will take precidence"
        if fn_name != '__call__': warnings.warn(wrn_msg)
    if DEBUG: print("MODULE BECOMES CALLABLE")
    module = CallableModule(module)
    # assert hasattr(module, '__call__')
    parent_module_fullname = '.'.join(module.__name__.split('.')[:-1])
    parent_module_name = module.__name__.split('.')[-1]
    sys.modules[module.__name__] = module
    if parent_module_fullname in sys.modules:
        sys.modules[parent_module_fullname].__setattr__(parent_module_name, module)
    return module


class CallableModule(ModuleType):
    def __init__(self, module):
        if DEBUG: print(">F> CallableModule.__init__")
        super().__init__(module.__name__)
        _original_module = sys.modules[module.__name__]
        object.__setattr__(self, '_original_module', _original_module)
        self.__dict__.update(_original_module.__dict__)


    def __getattr__(self, name):
        # DEBUG = True
        _original_module = object.__getattribute__(self, '_original_module')
        original_attr = None
        normal_attr = None
        if DEBUG: print(f"name: {name}")
        if name in self.__dict__:
            normal_attr = object.__getattribute__(self, name)
        attr_name = _original_module.__name__.split('.')[-1]
        if attr_name in _original_module.__dict__:
            middle_attr = object.__getattribute__(_original_module, attr_name)
            if name in middle_attr.__dict__:
                original_attr = object.__getattribute__(middle_attr, name)
        
        if normal_attr is not None and original_attr is not None:
            def1 = f"{_original_module.__name__}.{attr_name}.{name}"
            def2 = f"{self.__name__}.{name}"
            wrn_msg = f"~!~ Both {def1} and {def2} are defined. Defaulting to {def1}"
            if def1 != def2: warnings.warn(wrn_msg)
            return original_attr
        elif normal_attr is not None:
            return normal_attr
        elif original_attr is not None:
            return original_attr
        # This should and will raise an error:
        object.__getattribute__(self, name)


    def __call__(self, *args, **kwargs):
        if DEBUG: print(">F> CallableModule.__call__")
        og_module = object.__getattribute__(self, '_original_module')
        attr_name = og_module.__name__.split('.')[-1]
        foo_attr = None
        foo_call = None
        if attr_name in og_module.__dict__: 
            foo_attr = object.__getattribute__(og_module, attr_name)
            if DEBUG: print(f"foo_attr: {foo_attr}")
        if "__call__" in og_module.__dict__: 
            foo_call = object.__getattribute__(og_module, "__call__")
            if DEBUG: print(f"foo_call: {foo_call}")
        
        if foo_attr is not None and foo_call is not None:
            def1 = f"{self.__name__}.{attr_name}"
            def2 = f"{self.__name__}.__call__"
            wrn_msg = f"~!~ Both {def1} and {def2} are defined. Defaulting to {def1}"
            if def1 != def2: warnings.warn(wrn_msg)
            return foo_attr(*args, **kwargs)
        elif foo_attr is not None:
            return foo_attr(*args, **kwargs)
        elif foo_call is not None:
            return foo_call(*args, **kwargs)
        # This should and will raise an error:
        return super().__call__(*args, **kwargs)
            
            
    def __dir__(self):
        if DEBUG: print(">F> CallableModule.__dir__")
        module_attrs = super().__dir__()
        if VERBOSE: print(f">>> module_attrs: {module_attrs}")
        return sorted(list(set(module_attrs + ['__call__'])))
