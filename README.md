## CI Status

| Python | Status |
|--------|--------|
| 3.8 | ![3.8](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.8) |
| 3.9 | ![3.9](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.9) |
| 3.10 | ![3.10](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.10) |
| 3.11 | ![3.11](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.11) |
| 3.12 | ![3.12](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.12) |
| 3.13 | ![3.13](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.13) |
| 3.14 | ![3.14](https://github.com/Uomocosa/new-python-import-system/actions/workflows/tests.yml/badge.svg?job=Python%203.14) |


# Core Idea
**I dislike the python import system**.

_I want a package that I can import and it magically makes the import system smarter, and possibly to my liking_.

**After you import this package, and "install it" using `new_import_system.install(__file__)` in the top-level-init file of your package**:
- When you import a package, its subpackages, (if any) are lazy loaded automatically.
- If in a package/module you have a file/function named `__call__` or it has the same name as the package/module, then when you call the package/module that function gets automatically called.
- All `__init__.py` files in your project _should_ remain empty, I have not tested how they interact with this package.

# Usage
_**#TODO** Test exact usage, from `uv add new_python_import_system` or similar `uv add https:\\link-to-this-repo`._

In the "**root**" `__init__.py` file of your package, (The top-level-init file) you can import this package and use it to enhance your import system.
If we take as example the package `test/0_simple_package`, the top-level-init file is the `test/0_simple_package/pkg0/__init__.py`:
```python
import new_import_system
new_import_system.install(__file__)
```

### Tests
There are many tests in the `test` folder, they can be all run from `uv run -p .venv pytest`.

# Considerations
_**#TODO** I changed from using pip install -e . to using uv. The underneath considerations have to be rewritten._

I need to consider many different cases
- If this is called after some packages/modules have been initialized, what should I do? Should I reload them? Should I populate their attributes?
- If this is called from a python -m ... command (so the sys.path and sys.modules are populized)
- If this is called from a python ... command (so the sys.path and sys.modules are kinda empty)
- How do I define a top_level_package (should I search for the last `__init__.py` from parents folders, for `setup.py`? for `pyproject.toml`? What happens if I find multiples?)
- Is the functions I use general enouugh? Are they "correct"?
- I would like to add this import hook at the **END** of `sys.meta_path`, but at the moment it is not possible, and is instead added at the start.

Any help is kindly apprechiated :)

# Current answers for my considerations.
As of now I try to:
- Get the top_level_package and re-import it.
- Get the caller_file for when an import is called using the `inspect` library.
- Throw a warning if it menages to import a package/module, but it results in a "_too-magical approach_".
<!--- After you import this, every time you try to import a modules, if its a top-level package or subpackage it gets reloaded (_**ONLY ONCE PER PACKAGE**_). I do not know if `importlib.reload()` is fine to use ;;-->
