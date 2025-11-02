def test_0():
    print()
    import new_import_system
    import package.submodule1
    print(f"dir(package.submodule1): {dir(package.submodule1)}")
    print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")

def test_1():
    print()
    import new_import_system
    import package.submodule1.fun1
    print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")


# import pytest
# @pytest.mark.skip(reason="problem for later")
# def test_absolute_import():
#     import new_import_system
#     import package # HERE 'CallableFinder' is NOT called!
#     print(f"dir(package.submodule1): {dir(package.submodule1)}")
#     print(f"dir(package.submodule1.fun1): {dir(package.submodule1.fun1)}")
#     assert package.submodule1.fun1() == 'fun1'