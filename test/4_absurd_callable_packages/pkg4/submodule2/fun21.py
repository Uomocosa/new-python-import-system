"""
If you install this package using 'pip install .'
you can even run this file (like 'python fun21.py') and will work
NOTICE. You dont need to do python -m ...
ALSO.   Relative imports will still work!
WHY?    This can useful if someone wants to test this function 
        without doing pytest ..., they can just clik run on the
        vscode gui. 
HOWEVER.You need to import package every time, to do it
        Or at least do 'if __name__ == '__main__': import package'
        As a consolation, it is lazily loaded.
"""
import pkg4 
from ..submodule1 import fun11

def test_sys_modules(DEBUG=False):
    import sys
    if DEBUG: print(f"sys.modules[-15:]: {list(sys.modules.keys())[-15:]}")
    assert 'pkg4' in sys.modules

def __call__(DEBUG=False): 
    if DEBUG: print('fun21')
    assert fun11(DEBUG=DEBUG) == 'fun11'
    assert pkg4.callable_package(DEBUG=DEBUG) == 'callable_package/__call__'
    return 'fun21'

def test_(DEBUG=False):
    assert __call__(DEBUG=DEBUG) == 'fun21'

if __name__ == '__main__': 
    test_sys_modules(DEBUG=True)
    test_(DEBUG=True)
