from saveable_objects._meta_class import SaveAfterInitMetaClass

DEFAULT_PATH= "default_path"
PATH_STRING = "path_string"
assert PATH_STRING != DEFAULT_PATH

class TestClass(metaclass=SaveAfterInitMetaClass):
        def __init__(self, *args, path=None, **kwargs):
            self.saved_to_path = None
            self.args = args
            self.kwargs = kwargs
        def _save(self, path):
            self.saved_to_path = path
            
class DefaultPathTestClass(TestClass):
        _path: str = DEFAULT_PATH

class TestException(Exception): pass
class SaveFailureClass(metaclass=SaveAfterInitMetaClass):
        def __init__(self, *args, path=None, **kwargs): pass
        def _save(self, path):
            raise TestException()

def test_no_path():
    test_instance = TestClass()
    assert test_instance.saved_to_path is None
    assert test_instance.path is None

def test_with_path():
    test_instance = TestClass(path=PATH_STRING)
    assert test_instance.saved_to_path == PATH_STRING
    assert test_instance.path == PATH_STRING

def test_with_default_path_and_no_path():
    test_instance = DefaultPathTestClass()
    assert test_instance.saved_to_path == DEFAULT_PATH
    assert test_instance.path == DEFAULT_PATH

def test_with_default_path_and_path():
    test_instance = DefaultPathTestClass(path=PATH_STRING)
    assert test_instance.saved_to_path == PATH_STRING
    assert test_instance.path == PATH_STRING

def test_failure_to_save():
    failed = False
    try:
        test_instance = SaveFailureClass(path=PATH_STRING)
    except TestException:
        failed = True
    assert failed

def test_args_with_path():
    test_instance = TestClass(1, 2, 3, path=PATH_STRING)
    assert test_instance.args == (1, 2, 3)

def test_kwargs_with_path():
    test_instance = TestClass(path=PATH_STRING, four=4, five=5)
    assert test_instance.kwargs == {"four": 4, "five": 5}

def test_args_and_kwargs_with_path():
    test_instance = TestClass(1, 2, 3, path=PATH_STRING, four=4, five=5)
    assert test_instance.args == (1, 2, 3)
    assert test_instance.kwargs == {"four": 4, "five": 5}

def test_args_no_path():
    test_instance = TestClass(1, 2, 3)
    assert test_instance.args == (1, 2, 3)

def test_kwargs_no_path():
    test_instance = TestClass(four=4, five=5)
    assert test_instance.kwargs == {"four": 4, "five": 5}

def test_args_and_kwargs_no_path():
    test_instance = TestClass(1, 2, 3, four=4, five=5)
    assert test_instance.args == (1, 2, 3)
    assert test_instance.kwargs == {"four": 4, "five": 5}