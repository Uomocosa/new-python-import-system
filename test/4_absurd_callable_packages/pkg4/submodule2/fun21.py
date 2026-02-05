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
