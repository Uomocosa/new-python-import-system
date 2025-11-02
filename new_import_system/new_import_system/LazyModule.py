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
    def __init__(self, full_import_name: str, abs_Path: Path):
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
        return self._module(*args, **kwargs)
        



