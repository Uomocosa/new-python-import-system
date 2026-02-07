## CI Status

| Python | Status |
|--------|--------|
| 3.8 | ![3.8](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-8.yml/badge.svg) |
| 3.9 | ![3.9](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-9.yml/badge.svg) |
| 3.10 | ![3.10](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-10.yml/badge.svg) |
| 3.11 | ![3.11](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-11.yml/badge.svg) |
| 3.12 | ![3.12](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-12.yml/badge.svg) |
| 3.13 | ![3.13](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-13.yml/badge.svg) |
| 3.14 | ![3.14](https://github.com/Uomocosa/new-python-import-system/actions/workflows/test-3-14.yml/badge.svg) |


# Core Idea
**I dislike the python import system**.

_I want a package that I can import and it magically makes the import system smarter, and possibly to my liking_.

**After you import this package, and "install it" using `new_import_system.install(__file__)` in the top-level-init file of your package**:
- When you import a package, its subpackages, (if any) are lazy loaded automatically.
- If in a package/module you have a file/function named `__call__` or it has the same name as the package/module, then when you call the package/module that function gets automatically called.
- All `__init__.py` files in your project _should_ remain empty, I have not tested how they interact with this package.

# Usage
Using [uv](https://docs.astral.sh/uv/getting-started/installation/): 
- In the dependencies section of your `project.toml` file add `"new-import-system @ git+https://github.com/Uomocosa/new-python-import-system"`
- Or use `uv add new-import-system @ git+https://github.com/Uomocosa/new-python-import-system`

In the "**root**" `__init__.py` file of your package, (The top-level-init file) you can import this package and use it to enhance your import system.
If we take as example the package `test/0_simple_package`, the top-level-init file is the `test/0_simple_package/pkg0/__init__.py`:
```python
import new_import_system
new_import_system.install(__file__)
```

# Tests
There are many tests in the `test` folder, they can be all run from `uv run -p .venv pytest`.

# As of now I:
- Get the top_level_package by forcing the user to use the `.install(__file__)` function. This should be acceptable, as it is a one-time operation, and make the package less _magical_.
- Based on the path of the top-level-init file, this package adds a import hook that allows you to import your sub-modules much more easily. Using this I can create much more files with a single function or class and test it inside the same file.

# TODO
_**Any help is kindly apprechiated :)**_
_Add tests for each of the following cases_
- Test with large imports like `import torch` see how time it takes to `.install()`
- I dislike using lele.type(path.to.Class) or having to use path.to.Class.Class to define the type
- Change the way DEBUG and VERBOSE work, I like to have a better way to control the verbosity of the package. Possibly by using loguru.
- Improve the error messages when an import fails.
