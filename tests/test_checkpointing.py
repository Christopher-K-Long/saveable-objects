import os
import threading
import datetime
import inspect

from saveable_objects import SaveableObject
from saveable_objects.checkpointing import failed, succeeded

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SAVE_DIR = os.path.join(TEST_DIR, "__test_write_directory__")

class UniquePath():
    def __init__(self):
        thread_id = threading.current_thread().ident
        datetime.datetime.now().strftime("%Z%Y%m%d%H%M%S%f")
        self.unique_path = os.path.join(SAVE_DIR, f"calling_function_{__name__}_{inspect.stack()[1][3]}__thread_id_{thread_id}__datetime_{datetime.datetime.now().strftime('%Z%Y%m%d%H%M%S%f')}.pkl")
    def __enter__(self):
        return self.unique_path
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if os.path.exists(self.unique_path):
            os.remove(self.unique_path)

def test_failed_load():
    with UniquePath() as path:
        SaveableObject(path=path)
        assert not failed(SaveableObject.load(path=path))

def test_succeeded_load():
    with UniquePath() as path:
        SaveableObject(path=path)
        assert succeeded(SaveableObject.load(path=path))

def test_failed_load_if():
    assert failed(SaveableObject.loadif())
    with UniquePath() as path:
        assert failed(SaveableObject.loadif(path=path))
        assert not failed(SaveableObject.loadif(path=path))

def test_succeeded_load_if():
    assert not succeeded(SaveableObject.loadif())
    with UniquePath() as path:
        assert not succeeded(SaveableObject.loadif(path=path))
        assert succeeded(SaveableObject.loadif(path=path))

def test_failed_loadifparams():
    assert failed(SaveableObject.loadifparams())
    with UniquePath() as path:
        assert failed(SaveableObject.loadifparams(path=path))
        assert not failed(SaveableObject.loadifparams(path=path))

def test_succeeded_loadifparams():
    assert not succeeded(SaveableObject.loadifparams())
    with UniquePath() as path:
        assert not succeeded(SaveableObject.loadifparams(path=path))
        assert succeeded(SaveableObject.loadifparams(path=path))

def test_failed_tryload():
    with UniquePath() as path:
        assert failed(SaveableObject.tryload(path=path))
        SaveableObject(path=path)
        assert not failed(SaveableObject.tryload(path=path))

def test_succeeded_tryload():
    with UniquePath() as path:
        assert not succeeded(SaveableObject.tryload(path=path))
        SaveableObject(path=path)
        assert succeeded(SaveableObject.tryload(path=path))