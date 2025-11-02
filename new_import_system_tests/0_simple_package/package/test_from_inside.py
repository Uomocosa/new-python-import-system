def test_get_importer_filepath():
    import new_import_system
    from pathlib import Path
    assert new_import_system.get_importer_filepath() == Path(__file__).absolute()

def test_1():
    import new_import_system
    import submodule1
    assert submodule1.fun1() == 'fun1'

def test_2():
    from submodule1 import fun1
    assert fun1() == 'fun1'

def test_3():
    from package import submodule1
    assert submodule1.fun1() == 'fun1'

# def test_4():
#     from package.submodule1 import fun1
#     assert fun1() == 'fun1'

# def test_5():
#     from . import submodule1
#     assert submodule1.fun1() == 'fun1'
    
# def test_6():
#     from .submodule1 import fun1
#     assert fun1() == 'fun1'
