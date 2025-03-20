import os
import threading
import datetime
import inspect

from saveable_objects import SaveableObject
from saveable_objects.extensions import SaveableWrapper

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SAVE_DIR = os.path.join(TEST_DIR, "__test_write_directory__")

TEST_VALUE = 42

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

def test_SaveableWrapper_class_get_item():
    class TestClass:
        def __init__(self, a):
            self.a = a
    SaveableTestClass = SaveableWrapper[TestClass];
    with UniquePath() as path:
        test_instance = SaveableTestClass(TEST_VALUE, path=path)
        test_instance2 = SaveableTestClass.load(path)
        assert test_instance.a == test_instance2.a

def test_SaveableWrapper_default_path_get_item():
    class TestClass:
        def __init__(self, a):
            self.a = a
    with UniquePath() as path:
        SaveableWrapperPath = SaveableWrapper(path=path)
        assert SaveableObject.tryload(path) == False
        SaveableTestClass = SaveableWrapperPath[TestClass];
        test_instance = SaveableTestClass(TEST_VALUE)
        test_instance2 = SaveableTestClass.load(path)
        assert test_instance.a == test_instance2.a

def test_SaveableWrapper_default_path_call():
    class TestClass:
        def __init__(self, a):
            self.a = a
    with UniquePath() as path:
        SaveableTestClass = SaveableWrapper(TestClass, path=path)
        assert SaveableObject.tryload(path) == False
        test_instance = SaveableTestClass(TEST_VALUE)
        test_instance2 = SaveableTestClass.load(path)
        assert test_instance.a == test_instance2.a

def test_SaveableWrapper_decorating():
    @SaveableWrapper
    class SaveableTestClass:
        def __init__(self, a):
            self.a = a
    with UniquePath() as path:
        test_instance = SaveableTestClass(TEST_VALUE, path=path)
        test_instance2 = SaveableTestClass.load(path)
        assert test_instance.a == test_instance2.a

def test_SaveableWrapper_decorating():
    with UniquePath() as path:
        @SaveableWrapper(path=path)
        class SaveableTestClass:
            def __init__(self, a):
                self.a = a
        assert SaveableObject.tryload(path) == False
        test_instance = SaveableTestClass(TEST_VALUE, path=path)
        test_instance2 = SaveableTestClass.load(path)
        assert test_instance.a == test_instance2.a