import new_import_system
from pkg3.submodule1 import fun11

def __call__(DEBUG=False): 
    if DEBUG: print('callable_package/__call__')
    assert fun11(DEBUG=DEBUG) == 'fun11'
    return 'callable_package/__call__'

def test_():
    assert __call__(DEBUG=True) == 'callable_package/__call__'
