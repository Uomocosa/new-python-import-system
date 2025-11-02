# import importlib
# from pathlib import Path
# from types import ModuleType
# from .P import P

# DEBUG = True

# class LazyModule(ModuleType):
#     """
#     A proxy class that delays the import of a module until its first use.
#     """
#     def __init__(self, full_import_name: str, abs_Path: Path):
#         if DEBUG: print(f">F> __init__")
#         name = full_import_name.split('.')[-1]
#         super().__init__(name)
#         self._full_import_name = full_import_name # ex.: package.subpackage.module
#         self._module = None
#         self.__file__ = abs_Path
#         self.__name__ = name

#     def __call__(self, *args, **kwargs):
#         self._load()
#         if '__call__' in self._module.__dict__:
#             foo = self._module.__dict__['__call__']
#             return foo(*args, **kwargs)
#         if self.__name__ in self._module.__dict__:
#             foo = self._module.__dict__[self.__name__]
#             return foo(*args, **kwargs)
#         err_msg  = f"module: '{self.__name__}' is not callable"
#         if P(self.__file__).is_dir():
#             err_msg += f"\n~!~ This is a PACKAGE (or folder), located at:"
#             err_msg += f"\n~!~ '{self.__file__}'"
#             err_msg += f"\n~!~ TO MAKE IT CALLABLE, please create a file '__call__.py' and"
#             err_msg += f"\n~!~ inside of it define a '__call__' function."
#             err_msg += f"\n~!~ Then, when you call this module that function will be invoked"
#         elif P(self.__file__).is_file():
#             err_msg += f"\n~!~ !!!NOT YET IMPLMENTED!!!"
#             err_msg += f"\n~!~ This is a MODULE (or file), located at:"
#             err_msg += f"\n~!~ '{self.__file__}'"
#             err_msg += f"\n~!~ TO MAKE IT CALLABLE: define a funtion '__call__'"
#             err_msg += f"\n~!~ OR: a funtion with the same name ('{self.__name__}')"
#             err_msg += f"\n~!~ Then, when you call this module that function will be invoked"
#         raise TypeError(err_msg)

#     def __getattr__(self, name):
#         """
#         This magic method is called *only* when an attribute
#         is not found on the LazyModule instance itself.
        
#         It's the trigger for our lazy loading.
#         """
#         if not self._module: self._load()
#         return getattr(self._module, name)

#     def __repr__(self):
#         """Provides a helpful string representation for debugging."""
#         status = "loaded" if self._module is not None else "not loaded"
#         return f"<LazyModule '{self._module_name}' ({status})>"

#     def __setattr__(self, name, value):
#         if name in ('_module_name', '_module'): # not sure about this
#             super().__setattr__(name, value)
#         else:
#             self._load()
#             setattr(self._module, name, value)

#     def __delattr__(self, name):
#         self._load()
#         delattr(self._module, name)


# def load_LazyModule(LazyModule):
