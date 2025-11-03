# new_import_sytem
This is the library you have to import.
1. Activate your `venv`
2. cd to this folder
3. `pip install -e .`

# Testing
To run the tests:
1. Install this library/package as mentioned above
2. `pip install pytest`
3. `cd ../new_import_system_tests`

To run a single test: (example)
`python -m pytest "0_simple_package/package/test_from_inside.py::test_0"`

To run all tests in a file: (example)
`python -m pytest "0_simple_package/package/test_from_inside.py"`

To run all tests_files in a folder: (example)
`python -m pytest "0_simple_package"`

To run ALL tests_files:
`python run_external_tests.py`