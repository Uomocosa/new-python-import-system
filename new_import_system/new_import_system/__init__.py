# This is the __init__.py that get's called when you import this package!
import sys
import os
import inspect
import warnings
import importlib.util
import importlib.abc
from types import ModuleType
from pathlib import Path

def P(path) -> Path: return Path(path).resolve()

DEBUG = True
VERBOSE = False

THIS_FILE_PATH = P(__file__)
if DEBUG: print(f">>> THIS_FILE_PATH: {THIS_FILE_PATH}")


class CallableFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if DEBUG: print(f">F> CallableFinder's find_spec")
        if DEBUG: print(f">>> self: {self}")
        if DEBUG: print(f">>> fullname: {fullname}")
        if DEBUG: print(f">>> path: {path}")
        if DEBUG: print(f">>> target: {target}")
        if DEBUG: print(f">>> get_importer_filepath(): {get_importer_filepath()}")
        importer_file = get_importer_filepath()
        if path is None: # Top-level import (~ex.: 'import module1')
            if not importer_file: 
                if DEBUG: print(">>> No importer file, returning None")
                return None
            search_dirs = [importer_file.parent]
            module_name_to_find = fullname # e.g., 'submodule1'
        else: # Submodule import (~ex.: 'from module1 import submodule1')
            search_dirs = path # e.g., ['.../package']
            module_name_to_find = fullname.split('.')[-1] # e.g., 'submodule1'
        base_dirs = [P(base_dir_str) for base_dir_str in search_dirs]
        files_to_import = [dir / f"{module_name_to_find}.py" for dir in base_dirs]
        packages_to_import = [dir / module_name_to_find / "__init__.py" for dir in base_dirs]
        files_to_import = [f for f in files_to_import if f.exists()]
        packages_to_import = [d for d in packages_to_import if d.exists()]
        assert len(files_to_import) <= 1, "How are there more than 1 FILE with the same name in this folder???"
        assert len(packages_to_import) <= 1, "How are there more than 1 PACKAGE with the same name in this folder???"
        if files_to_import and packages_to_import:
            warnings.warn(f"Found both a file and a python package named {fullname}, I will import the python package")
        if packages_to_import:
            package_to_import = packages_to_import[0]
            spec = importlib.util.spec_from_file_location(
                fullname,
                package_to_import,
                submodule_search_locations=[str(importer_file.parent / fullname)] 
            )
        elif files_to_import:
            file_to_import = files_to_import[0]
            spec = importlib.util.spec_from_file_location(
                fullname,
                file_to_import
            )
        else: return None
        if DEBUG: print(f">>> spec.loader: {spec.loader}")
        if spec.loader:
            if DEBUG: print(f">>> Wrapping loader for {fullname} with CallableLoader")
            # TODO
            # spec.loader = CallableLoader(spec.loader)
        return spec





def get_importer_filepath() -> Path:
    """
    Walks the stack to find the first frame that 
    is NOT part of the importlib machinery.
    """
    import_frames = inspect.stack()
    import_frames = [x for x in import_frames if not x.filename.startswith("<frozen importlib")]
    import_frames = [x for x in import_frames if not Path(x.filename) == THIS_FILE_PATH]
    if DEBUG and VERBOSE: [print(frame.filename) for frame in import_frames]
    if not import_frames: return None
    return P(import_frames[0].filename)




def install_hook():
    """Prepends our custom finder to the meta_path."""
    if DEBUG: print(">>> new_import_system's hook installed")
    if not any(isinstance(f, CallableFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, CallableFinder())

install_hook()