import subprocess
import sys
import os
from pathlib import Path

# Find all immediate subdirectories in the 'tests' folder
# that don't start with an underscore or dot.
p = Path('.').absolute()
dirs = [dir for dir in p.iterdir() if dir.is_dir()]
# print(dirs)
python_packages = [dir for dir in dirs if (dir / "__init__.py").exists()]
# print(python_packages)
relative_packages = [dir.relative_to(p) for dir in python_packages]
# print(relative_packages)

run_test_dir = lambda dir: subprocess.run([sys.executable, "-m", "pytest", dir], text=True)

results = [run_test_dir(dir) for dir in sorted(relative_packages)]
retunrcodes = [r.returncode for r in results]
if any(retunrcodes): exit(1)
