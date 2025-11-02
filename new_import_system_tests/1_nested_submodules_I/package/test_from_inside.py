def test_fun11_I():
    import new_import_system
    import submodule1
    assert submodule1.fun11() == 'fun11'

def test_fun11_II():
    import new_import_system
    from submodule1 import fun11
    assert fun11() == 'fun11'

def test_fun11_III():
    import new_import_system
    from package import submodule1
    assert submodule1.fun11() == 'fun11'

def test_fun11_IV():
    import new_import_system
    from package.submodule1 import fun11
    assert fun11() == 'fun11'

def test_fun11_V():
    import new_import_system
    from . import submodule1
    assert submodule1.fun11() == 'fun11'
    
def test_fun11_VI():
    import new_import_system
    from .submodule1 import fun11
    assert fun11() == 'fun11'
