import sys
from types import ModuleType

DEBUG = False

def make_module_callable(module, DEBUG=False, VERBOSE=False):
    if DEBUG: print(f">F> make_module_callable")
    if VERBOSE: print(f">>> dir(module): {dir(module)}")
    fn_name = module.__name__.split('.')[-1]
    if DEBUG: print(f">>> fn_name: {fn_name}")
    if not hasattr(module, fn_name): return module
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
        return call_this(self, *args, **kwargs)
    
    def __dir__(self):
        module_attrs = super().__dir__()
        class_attrs = object.__dir__(self)
        return sorted(list(set(module_attrs + class_attrs)))


def call_this(module, *args, **kwargs):
    if DEBUG: print(f">F> call_this")
    fn_name = module.__name__.split('.')[-1]
    if hasattr(module, fn_name):
        foo = getattr(module, fn_name)
        return foo(*args, **kwargs)
    
    err_msg  = f"self: '{module.__name__}' is not callable"
    if module.__file__.endswith('__init__.py'):
        err_msg += f"\n~!~ This is a PACKAGE (or folder), located at:"
        err_msg += f"\n~!~ '{module.__file__}'"
        err_msg += f"\n~!~ TO MAKE IT CALLABLE, please create a file '__call__.py' and"
        err_msg += f"\n~!~ inside of it define a '__call__' function."
        err_msg += f"\n~!~ Then, when you call this self that function will be invoked"
    elif module.__file__.endswith('.py'):
        err_msg += f"\n~!~ !!!NOT YET IMPLMENTED!!!"
        err_msg += f"\n~!~ This is a MODULE (or file), located at:"
        err_msg += f"\n~!~ '{module.__file__}'"
        err_msg += f"\n~!~ TO MAKE IT CALLABLE: define a funtion '__call__'"
        err_msg += f"\n~!~ OR: a funtion with the same name ('{fn_name}')"
        err_msg += f"\n~!~ Then, when you call this module that function will be invoked"
    raise TypeError(err_msg)
