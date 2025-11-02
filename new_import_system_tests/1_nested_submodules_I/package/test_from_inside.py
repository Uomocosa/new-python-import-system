def test_imports_I():
    import new_import_system
    import package.submodule1
    assert 'fun11' in dir(package.submodule1)
    print(f"dir(package.submodule1): {dir(package.submodule1)}")


# def test_imports_II():
#     import new_import_system
#     import package.submodule1
#     print(f"dir(package.submodule1): {dir(package.submodule1)}")
#     print(f"dir(package.submodule1.subsub1): {dir(package.submodule1.subsub1)}")
#     print(f"dir(package.submodule1.subsub1.fun111): {dir(package.submodule1.subsub1.fun111)}")
    
# def test_fun111_I():
#     import new_import_system
#     import package.submodule1.subsub1.fun111
#     # print(f"dir(package.submodule1.subsub1.fun111): {dir(package.submodule1.subsub1.fun111)}")
#     # assert '__call__' in dir(package.submodule1.subsub1.fun111)
#     assert package.submodule1.subsub1.fun111() == 'fun111'


# def test_fun111_II():
#     import new_import_system
#     import package.submodule1
#     assert package.submodule1.subsub1.fun111() == 'fun111'

# def test_fun11_I():
#     import new_import_system
#     import package.submodule1
#     assert package.submodule1.fun11() == 'fun11'
