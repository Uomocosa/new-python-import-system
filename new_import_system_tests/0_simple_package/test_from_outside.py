def test_1():
    import package
    assert package.submodule1.fun1() == 'fun1'

def test_2():
    from package import submodule1
    assert submodule1.fun1() == 'fun1'

def test_3():
    from package.submodule1 import fun1
    assert fun1() == 'fun1'
