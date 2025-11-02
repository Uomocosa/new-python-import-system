def test_fun11_I():
    import new_import_system
    import package
    assert package.submodule1.fun11() == 'fun11'

def test_fun11_II():
    import new_import_system
    from package import submodule1
    assert submodule1.fun11() == 'fun11'

def test_fun11_III():
    import new_import_system
    from package.submodule1 import fun11
    assert fun11() == 'fun11'

def test_fun21_I():
    import new_import_system
    import package
    assert package.submodule2.fun21() == 'fun21'

def test_fun21_II():
    import new_import_system
    from package import submodule2
    assert submodule2.fun21() == 'fun21'

def test_fun21_III():
    import new_import_system
    from package.submodule2 import fun21
    assert fun21() == 'fun21'

def test_fun111_I():
    import new_import_system
    import package
    assert package.submodule1.subsub1.fun111() == 'fun111'

def test_fun111_II():
    import new_import_system
    from package import submodule1
    assert submodule1.subsub1.fun111() == 'fun111'

def test_fun111_III():
    import new_import_system
    from package.submodule1 import subsub1
    assert subsub1.fun111() == 'fun111'

def test_fun111_IV():
    import new_import_system
    from package.submodule1.subsub1 import fun111
    assert fun111() == 'fun111'