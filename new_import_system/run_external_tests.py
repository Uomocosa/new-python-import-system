"""
THIS IS BROKEN AT THE MOMENT!
USE 'new_import_systems_tests/run_external_tests.py'
"""

import subprocess
import sys
import os
from pathlib import Path

# Find all immediate subdirectories in the 'tests' folder
# that don't start with an underscore or dot.
project_root = Path('.').absolute().parent
test_dir =  project_root / "new_import_system_tests"
dirs = [dir for dir in test_dir.iterdir() if dir.is_dir()]
python_packages = [dir for dir in dirs if (dir / "__init__.py").exists()]
# print(python_packages)
relative_packages = [dir.relative_to(project_root) for dir in python_packages]
# print(relative_packages)

run_test_dir = lambda dir: subprocess.run(
    [sys.executable, "-m", "pytest", str(dir)],
    text=True,
    cwd=project_root,
)

results = [run_test_dir(dir) for dir in sorted(relative_packages)]
retunrcodes = [r.returncode for r in results]
if any(retunrcodes): exit(1)
