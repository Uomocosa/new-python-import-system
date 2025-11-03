import new_import_system
from ...submodule2 import fun21
import package

x111 = 'x111'

def fun111(DEBUG=False): 
    if DEBUG: print('fun111')
    assert fun21(DEBUG=DEBUG) == 'fun21'
    return 'fun111'

def test_():
    assert fun111(DEBUG=True) == 'fun111'
