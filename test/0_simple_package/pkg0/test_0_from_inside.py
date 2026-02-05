def test_0():
    import pkg0.submodule1
    assert hasattr(pkg0.submodule1, 'fun1')
    assert hasattr(pkg0.submodule1.fun1, 'fun1')
    # print(f"dir(pkg0.submodule1): {dir(pkg0.submodule1)}")
    # print(f"dir(pkg0.submodule1.fun1): {dir(pkg0.submodule1.fun1)}")

def test_1():
    import pkg0.submodule1.fun1
    assert hasattr(pkg0.submodule1.fun1, 'fun1')
    # print(f"dir(pkg0.submodule1.fun1): {dir(pkg0.submodule1.fun1)}")

def test_absolute_import():
    import pkg0
    # print(f"dir(pkg0): {dir(pkg0)}")
    # print(f"dir(pkg0.submodule1): {dir(pkg0.submodule1)}")
    # print(f"dir(pkg0.submodule1.fun1): {dir(pkg0.submodule1.fun1)}")
    assert pkg0.submodule1.fun1() == 'fun1'

def test_types_I():
    from types import ModuleType
    import pkg0.submodule1
    assert isinstance(pkg0.submodule1, ModuleType)
    assert isinstance(pkg0.submodule1.fun1, ModuleType)

def test_types_II():
    from types import ModuleType
    import pkg0
    assert isinstance(pkg0, ModuleType)
    assert isinstance(pkg0.submodule1, ModuleType)
    assert isinstance(pkg0.submodule1.fun1, ModuleType)
