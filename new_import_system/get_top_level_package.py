from .get_importers_stack import get_importers_stack

def get_top_level_package(DEBUG=False, VERBOSE=False):
    importers = get_importers_stack()
    if VERBOSE: print(">>> importers: "); [print(f">>    {x}") for x in importers]
    top_package_init = importers[3]
    assert top_package_init.name == "__init__.py", "Install new_importer_system inside the '__init__.py' of your top level package of your project"
    if DEBUG: print(f"top_package_init: {top_package_init}")
    return top_package_init.parent