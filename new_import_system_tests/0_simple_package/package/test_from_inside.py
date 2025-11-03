def test_0():
    import package.submodule1
    assert hasattr(package.submodule1, 'fun1')
    assert hasattr(package.submodule1.fun1, 'fun1')
    # print(f"dir(package.submodule1): {dir(package.submodule1)}")
    # print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")

def test_1():
    import package.submodule1.fun1
    assert hasattr(package.submodule1.fun1, 'fun1')
    # print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")

def test_absolute_import():
    import package
    # print(f"dir(package): {dir(package)}")
    # print(f"dir(package.submodule1): {dir(package.submodule1)}")
    # print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")
    assert package.submodule1.fun1() == 'fun1'

def test_types_I():
    from types import ModuleType
    import package.submodule1
    assert isinstance(package.submodule1, ModuleType)
    assert isinstance(package.submodule1.fun1, ModuleType)

def test_types_II():
    from types import ModuleType
    import package
    assert isinstance(package, ModuleType)
    assert isinstance(package.submodule1, ModuleType)
    assert isinstance(package.submodule1.fun1, ModuleType)
