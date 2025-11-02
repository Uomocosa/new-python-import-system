import inspect
from importlib import Path

def P(path) -> Path: return Path(path).absolute()

INIT_FILE_PATH = P(__file__).parent / "__init__".py

# Works fine, but is a little hacky
def get_importer_filepath(DEBUG=False, VERBOSE=False) -> Path:
    """
    Walks the stack to find the first frame that 
    is NOT part of the importlib machinery.
    """
    import_frames = inspect.stack()
    import_frames = [x for x in import_frames if not x.filename.startswith("<frozen importlib")]
    import_frames = [x for x in import_frames if not Path(x.filename) == INIT_FILE_PATH]
    if DEBUG and VERBOSE: [print(frame.filename) for frame in import_frames]
    if not import_frames: return None
    return P(import_frames[0].filename)