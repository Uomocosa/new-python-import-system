import new_import_system
# import package
# from . import __init__

def test_sys_modules(DEBUG=False):
    import sys; 
    if DEBUG: print(f"sys.modules[-15:]: {list(sys.modules.keys())[-15:]}")
    assert 'package' in sys.modules
    # If you do import package 
    # You will get the sys.modules['package']
    # It will NOT pass through the new_import_system

def __call__(DEBUG=False): 
    if DEBUG: print('fun21')
    # assert fun11(DEBUG=DEBUG) == 'fun11'
    # assert package.callable_package(DEBUG=DEBUG) == 'callable_package/__call__'
    return 'fun21'

def test_():
    assert __call__(DEBUG=True) == 'fun21'

if __name__ == '__main__': 
    test_sys_modules(DEBUG=True)
    test_(DEBUG=True)