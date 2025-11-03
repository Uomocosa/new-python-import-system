def test_imports_I():
    import package.submodule1
    assert 'fun11' in dir(package.submodule1)

def test_imports_II():
    import package.submodule1
    assert 'subsub1' in dir(package.submodule1)
    assert 'fun111' in dir(package.submodule1.subsub1)
    assert 'x111' in dir(package.submodule1.subsub1.fun111)
    
def test_fun111_I():
    import package.submodule1.subsub1.fun111
    assert hasattr(package.submodule1.subsub1.fun111, '__call__')
    assert '__call__' in dir(package.submodule1.subsub1.fun111)

def test_fun111_II():
    import package.submodule1.subsub1.fun111
    assert package.submodule1.subsub1.fun111() == 'fun111'

def test_fun111_III():
    import package.submodule1
    assert package.submodule1.subsub1.fun111() == 'fun111'


def test_fun11_I():
    import package.submodule1.fun11
    assert package.submodule1.fun11() == 'fun11'

def test_fun11_II():
    import package.submodule1
    assert package.submodule1.fun11() == 'fun11'

def test_fun11_III():
    from package.submodule1.fun11 import fun11
    assert fun11() == 'fun11'

def test_fun21_I():
    import package.submodule2.fun21
    assert package.submodule2.fun21() == 'fun21'

def test_callable_package_I():
    from . import callable_package
    assert callable_package() == 'callable_package/__call__'

def test_callable_package_II():
    import package
    assert package.callable_package() == 'callable_package/__call__'