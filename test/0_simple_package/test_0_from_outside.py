def test_1():
    import pkg0
    assert pkg0.submodule1.fun1() == 'fun1'

def test_2():
    from pkg0 import submodule1
    assert submodule1.fun1() == 'fun1'

def test_3():
    from pkg0.submodule1 import fun1
    assert fun1() == 'fun1'
