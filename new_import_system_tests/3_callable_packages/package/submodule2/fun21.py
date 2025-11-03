import new_import_system
from ..submodule1 import fun11

def __call__(DEBUG=False): 
    if DEBUG: print('fun21')
    assert fun11(DEBUG=DEBUG) == 'fun11'
    return 'fun21'

def test_():
    assert __call__(DEBUG=True) == 'fun21'