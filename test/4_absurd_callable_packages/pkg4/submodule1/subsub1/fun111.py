if __name__ == '__main__': import package
from ...submodule2 import fun21

x111 = 'x111'

def fun111(DEBUG=False): 
    if DEBUG: print('fun111')
    assert fun21(DEBUG=DEBUG) == 'fun21'
    return 'fun111'

def test_():
    assert fun111(DEBUG=True) == 'fun111'

if __name__ == '__main__': test_()