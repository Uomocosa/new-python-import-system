import importlib
from pathlib import Path
from types import ModuleType
from .P import P
from .make_module_callable import make_module_callable

DEBUG = False

class LazyModule(ModuleType):
    """
    A proxy class that delays the import of a module until its first use.
    """
    def __init__(self, full_import_name: str, abs_Path: Path, x=None):
        if x is not None:
            err_msg =  f"Passed 4 arguments to LazyModule.__init__()\n"
            err_msg += f"Probably during inheritance\n"
            err_msg += f"Not implemented yet, play around it\n"
            raise NotImplementedError("")
        if DEBUG: print(f">F> __init__")
        name = full_import_name.split('.')[-1]
        super().__init__(name)
        object.__setattr__(self, 'D', DEBUG)
        object.__setattr__(self, '_full_import_name', full_import_name)
        object.__setattr__(self, '_module', None)
        object.__setattr__(self, '__file__', abs_Path)
        object.__setattr__(self, '__name__', name)
        if DEBUG: print(f">>> __init__ finished")

    def _load(self):
        """
        As this function is accessed the LazyModule gets 
        then REPLACED by a real "standard" module.
        """
        if DEBUG: print(f">F> ({self.__name__}) LazyModule's _load")
        self._module = importlib.import_module(self._full_import_name)
        self._module = make_module_callable(self._module, DEBUG=DEBUG)

    def __getattr__(self, name):
        if DEBUG: print(f">F> LazyModule's __getattr__({name})")
        if name in self.__dict__: return super().__getattr__(name, name)
        self._load()
        return getattr(self._module, name)

    def __setattr__(self, name, value):
        if DEBUG: print(f">F> LazyModule's __setattr__({name}, {value})")
        if name in self.__dict__: 
            self.__dict__[name] = value
        else:
            self._load()
            setattr(self._module, name, value)

    def __delattr__(self, name):
        if DEBUG: print(f">F> LazyModule's __delattr__({name})")
        self._load()
        delattr(self._module, name)

    def __dir__(self):
        if DEBUG: print(f">F> LazyModule's __dir__")
        self._load()
        if DEBUG: print(f">>> type(self._module): {type(self._module)}")
        if DEBUG: print(f">>> returning dir")
        return self._module.__dir__()
    
    def __repr__(self):
        if DEBUG: print(f">F> LazyModule's __repr__")
        self._load()
        return self._module.__repr__()
    
    def __str__(self):
        if DEBUG: print(f">F> LazyModule's __str__")
        self._load()
        return self._module.__str__()
    
    def __call__(self, *args, **kwargs):
        if DEBUG: print(f">F> LazyModule's __call__")
        self._load()
        try:
            return self._module(*args, **kwargs)
        except TypeError as e:
            if not "'module' object is not callable" in str(e): raise e
            err_msg  = f"self: '{self._module.__name__}' is not callable"
            if self._module.__file__.endswith('__init__.py'):
                err_msg += f"\n~!~ This is a PACKAGE (or folder), located at:"
                err_msg += f"\n~!~ '{self._module.__file__}'"
                err_msg += f"\n~!~ TO MAKE IT CALLABLE, please create a file '__call__.py' and"
                err_msg += f"\n~!~ inside of it define a '__call__' function."
                err_msg += f"\n~!~ Then, when you call this module that function will be invoked"
            elif self._module.__file__.endswith('.py'):
                err_msg += f"\n~!~ !!!NOT YET IMPLMENTED!!!"
                err_msg += f"\n~!~ This is a MODULE (or file), located at:"
                err_msg += f"\n~!~ '{self._module.__file__}'"
                err_msg += f"\n~!~ TO MAKE IT CALLABLE: define a funtion '__call__'"
                err_msg += f"\n~!~ OR: a funtion with the same name ('{self._module.__name__}')"
                err_msg += f"\n~!~ Then, when you call this module that function will be invoked"
            raise TypeError(err_msg)
