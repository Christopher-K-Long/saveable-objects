from typing import TypeVar, Generic

from .._saveable_object import SaveableObject
from .._meta_class import SaveAfterInitMetaClass

T = TypeVar("T")

class MetaSaveableWrapper(SaveAfterInitMetaClass):
    """A metaclass for the `SaveableWrapper` class.`
    """
    pass

class SaveableWrapper(Generic[T], SaveableObject, metaclass=MetaSaveableWrapper):
    """A template class for converting a general class to a ``SaveableObject``.
    For example a class ``T`` can be made into a new Saveable class
    ``SaveableT`` in any of the following ways:

    .. code-block:: python
    
        SaveableT = SaveableWrapper[T];
        SaveableT = SaveableWrapper(T, path="default_path.pkl")
        SaveableT = SaveableWrapper(path="default_path.pkl")[T];

    A default path for the ``SaveableObject`` can be set with the ``path``
    argument if parentheses are used.

    The new class ``SaveableT`` will inherited from both ``T`` and
    ``SaveableObject``.
    """