import new_import_system
from ..submodule1 import fun11

def fun21(DEBUG=False): 
    if DEBUG: print('fun21')
    assert fun11(DEBUG=DEBUG) == 'fun11'
    return 'fun21'

def test_():
    assert fun21(DEBUG=True) == 'fun21'