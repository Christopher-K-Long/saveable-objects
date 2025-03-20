import os
import threading
import datetime
import inspect

import numpy as np

from saveable_objects import SaveableObject

FILE_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.dirname(FILE_DIR)
SAVE_DIR = os.path.join(TEST_DIR, "__test_write_directory__")

TEST_VALUE = 42
TEST_VALUE2 = "test"
assert TEST_VALUE != TEST_VALUE2

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

class TestClass(SaveableObject):
    def __init__(self, a, path=None):
        self.a = a
        super().__init__(path=path)

def test_init_no_path():
    test_instance = SaveableObject()
    assert test_instance.path is None

def test_init_with_path():
    with UniquePath() as path:
        test_instance = SaveableObject(path=path)
        assert test_instance.path == path

def test_init_with_path_save():
    with UniquePath() as path:
        SaveableObject(path=path)
        assert os.path.exists(path)

def test_update_path():
    with UniquePath() as path:
        test_instance = SaveableObject(path=path)
        with UniquePath() as path2:
            test_instance.path = path2
            assert test_instance.path == path2

def test_update_path_save():
    with UniquePath() as path:
        test_instance = SaveableObject(path=path)
        with UniquePath() as path2:
            test_instance.path = path2
            assert not os.path.exists(path2)
            test_instance.save()
            assert os.path.exists(path2)

def test_save_to_different_path():
    with UniquePath() as path:
        test_instance = SaveableObject(path=path)
        with UniquePath() as path2:
            test_instance.save(path2)
            assert os.path.exists(path2)

def test_name():
    with UniquePath() as path:
        test_instance = SaveableObject(path=path)
        assert test_instance.name == os.path.split(os.path.splitext(path)[0])[-1]

def test_update_save():
    with UniquePath() as path:
        test_instance, success = TestClass.loadifparams(TEST_VALUE, path=path)
        assert not success
        test_instance.a = TEST_VALUE2
        test_instance.update_save()
        test_instance2, success = TestClass.loadifparams(TEST_VALUE, path=path)
        assert success
        assert test_instance2.a == TEST_VALUE2

def test_load():
    with UniquePath() as path:
        test_instance = TestClass(TEST_VALUE, path=path)
        test_instance2 = TestClass.load(path)
        assert test_instance.a == test_instance2.a

def test_lambda_save_and_load():
    f = lambda x: 2*x
    with UniquePath() as path:
        test_instance = TestClass(f, path=path)
        test_instance2 = TestClass.load(path)
        assert test_instance.a(2) == test_instance2.a(2)

def test_numpy_save_and_load():
    f = np.array([[1, 2], [3,2]])
    with UniquePath() as path:
        test_instance = TestClass(f, path=path)
        test_instance2 = TestClass.load(path)
        assert np.array_equal(test_instance.a, test_instance2.a)

def test_strict_typing():
    with UniquePath() as path:
        SaveableObject(path=path)
        failed = False
        try:
            TestClass.load(path)
        except TypeError:
            failed = True
        assert failed

def test_no_strict_typing():
    with UniquePath() as path:
        SaveableObject(path=path)
        failed = False
        try:
            TestClass.load(path, strict_typing=False)
        except TypeError:
            failed = True
        assert not failed

def test_save_overwrite():
    with UniquePath() as path:
        test_instance = TestClass(TEST_VALUE, path=path)
        test_instance.a = TEST_VALUE2
        test_instance.save()
        test_instance2 = TestClass.load(path)
        assert test_instance2.a == TEST_VALUE2

def test_try_load_fail():
    with UniquePath() as path:
        assert not SaveableObject.tryload(path)

def test_try_load_fail():
    with UniquePath() as path:
        test_instance = TestClass(TEST_VALUE, path=path)
        test_instance2 = TestClass.tryload(path)
        assert test_instance2
        assert test_instance.a == test_instance2.a

def test_loadifparams():
    with UniquePath() as path:
        test_instance, success = TestClass.loadifparams(TEST_VALUE, path=path)
        assert not success
        test_instance2, success = TestClass.loadifparams(TEST_VALUE, path=path)
        assert success
        assert test_instance.a == test_instance2.a
        test_instance3, success = TestClass.loadifparams(TEST_VALUE2, path=path)
        assert not success
        assert test_instance3.a == TEST_VALUE2

def test_loadifparams_numpy():
    f = np.array([[1, 2], [3,2]])
    g = np.array([[1, 2, 3], [4, 3,2]])
    with UniquePath() as path:
        test_instance, success = TestClass.loadifparams(f, path=path)
        assert not success
        test_instance2, success = TestClass.loadifparams(f, path=path)
        assert success
        assert np.array_equal(test_instance.a, test_instance2.a)
        test_instance3, success = TestClass.loadifparams(g, path=path)
        assert not success
        assert np.array_equal(test_instance3.a, g)

def test_loadif_no_path():
    test_instance, success = TestClass.loadif(TEST_VALUE)
    assert not success
    assert test_instance.a == TEST_VALUE

def test_loadif_path():
    with UniquePath() as path:
        test_instance = TestClass(TEST_VALUE, path=path)
        test_instance2, success = TestClass.loadif(TEST_VALUE, path=path)
        assert success
        assert test_instance.a == test_instance2.a
    
def test_loadif_wrong_path():
    with UniquePath() as path:
        test_instance, success = TestClass.loadif(TEST_VALUE, path=path)
        assert not success
        assert test_instance.a == TEST_VALUE