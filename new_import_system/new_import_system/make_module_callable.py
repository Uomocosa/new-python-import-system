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
    assert hasattr(module, '__call__')
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
        self.__dict__.update(sys.modules[module.__name__].__dict__)

    def __call__(self, *args, **kwargs):
        if DEBUG: print(">F> CallableModule.__call__")
        return call_this(self, *args, **kwargs)
    
    def __dir__(self):
        if DEBUG: print(">F> CallableModule.__dir__")
        module_attrs = super().__dir__()
        if VERBOSE: print(f">>> module_attrs: {module_attrs}")
        return sorted(list(set(module_attrs + ['__call__'])))


def call_this(module, *args, **kwargs):
    if DEBUG: print(f">F> call_this")
    fn_name = module.__name__.split('.')[-1]
    if fn_name in module.__dict__: foo = module.__dict__[fn_name]
    if '__call__' in module.__dict__: foo = module.__dict__['__call__']
    if DEBUG: print(f"foo: {foo}")
    return foo(*args, **kwargs)

