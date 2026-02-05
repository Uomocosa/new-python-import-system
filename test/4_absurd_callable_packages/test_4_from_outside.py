def test_fun11_I():
    import pkg4
    assert pkg4.submodule1.fun11() == 'fun11'

def test_fun11_II():
    from pkg4 import submodule1
    assert submodule1.fun11() == 'fun11'

def test_fun11_III():
    from pkg4.submodule1 import fun11
    assert fun11() == 'fun11'

def test_fun21_I():
    import pkg4
    assert pkg4.submodule2.fun21() == 'fun21'

def test_fun21_II():
    from pkg4 import submodule2
    assert submodule2.fun21() == 'fun21'

def test_fun21_III():
    from pkg4.submodule2 import fun21
    assert fun21() == 'fun21'

def test_fun111_I():
    import pkg4
    assert pkg4.submodule1.subsub1.fun111() == 'fun111'

def test_fun111_II():
    from pkg4 import submodule1
    assert submodule1.subsub1.fun111() == 'fun111'

def test_fun111_III():
    from pkg4.submodule1 import subsub1
    assert subsub1.fun111() == 'fun111'

def test_fun111_IV():
    from pkg4.submodule1.subsub1 import fun111
    assert fun111() == 'fun111'

def test_callable_package_I():
    import pkg4
    assert pkg4.callable_package() == 'callable_package/__call__'
