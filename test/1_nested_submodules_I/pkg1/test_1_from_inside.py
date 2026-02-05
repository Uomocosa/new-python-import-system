def test_imports_I():
    import pkg1.submodule1
    assert 'fun11' in dir(pkg1.submodule1)

def test_imports_II():
    import pkg1.submodule1
    assert 'subsub1' in dir(pkg1.submodule1)
    assert 'fun111' in dir(pkg1.submodule1.subsub1)
    assert 'x111' in dir(pkg1.submodule1.subsub1.fun111)
    
def test_fun111_I():
    import pkg1.submodule1.subsub1.fun111
    assert hasattr(pkg1.submodule1.subsub1.fun111, '__call__')
    assert '__call__' in dir(pkg1.submodule1.subsub1.fun111)

def test_fun111_II():
    import pkg1.submodule1.subsub1.fun111
    assert pkg1.submodule1.subsub1.fun111() == 'fun111'

def test_fun111_III():
    import pkg1.submodule1
    assert pkg1.submodule1.subsub1.fun111() == 'fun111'


def test_fun11_I():
    import pkg1.submodule1.fun11
    assert pkg1.submodule1.fun11() == 'fun11'

def test_fun11_II():
    import pkg1.submodule1
    assert pkg1.submodule1.fun11() == 'fun11'

def test_fun11_III():
    from pkg1.submodule1.fun11 import fun11
    assert fun11() == 'fun11'

def test_fun21_I():
    import pkg1.submodule2.fun21
    assert pkg1.submodule2.fun21() == 'fun21'
