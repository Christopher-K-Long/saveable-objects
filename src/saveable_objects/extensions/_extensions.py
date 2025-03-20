from typing import Optional, TypeVar, Generic

from .._saveable_object import SaveableObject
from .._meta_class import SaveAfterInitMetaClass

T = TypeVar("T")

class MetaSaveableWrapper(SaveAfterInitMetaClass):
    """A metaclass for the :class:`SaveableWrapper` class.`
    """
    def __call__(cls, class_to_wrap: Optional[type] = None, path: Optional[str] = None):
        instance = type.__call__(cls, class_to_wrap, path)
        if class_to_wrap is None:
            return instance
        else:
            return instance[class_to_wrap]

class SaveableWrapper(Generic[T], SaveableObject, metaclass=MetaSaveableWrapper):
    """A template class for converting a general class to a
    :class:`SaveableObject <saveable_objects.SaveableObject>`. For example a
    class ``T`` can be made into a new Saveable class ``SaveableT`` in any of
    the following ways:

    .. code-block:: python
    
        SaveableT = SaveableWrapper[T];
        SaveableT = SaveableWrapper(T, path="default_path.pkl")
        SaveableT = SaveableWrapper(path="default_path.pkl")[T];

    A default path for the
    :class:`SaveableObject <saveable_objects.SaveableObject>` can be set with
    the ``path`` argument if parentheses are used.

    The new class ``SaveableT`` will inherited from both ``T`` and
    :class:`SaveableObject <saveable_objects.SaveableObject>`.
    """
    @staticmethod
    def _get_class(arg: type, path_initialiser: Optional[str] = None):
        class SaveableWrapped(arg, SaveableObject):
            """Initialises the object of type ``T`` and next the
            ``SaveableObject`` so that the initialisation of ``T`` is saved to
            the file at ``path``.

            Parameters
            ----------
            *args
                The arguments to pass to the initialisation.
            path : str, optional
                File path to save the object to. If ``None`` then the object is
                not saved. By default ``path_initialiser``
            **kwargs
                The keyword arguments to pass to the initialisation.
            """
            def __init__(self, *args, path: Optional[str] = path_initialiser, **kwargs):
                arg.__init__(self, *args, **kwargs)
                SaveableObject.__init__(self, path)
        return SaveableWrapped
    def __class_getitem__(cls, arg: type):
        return cls._get_class(arg)
    def __getitem__(self, arg: type):
        return self._get_class(arg, self.default_path)
    def __call__(self, arg: type):
        return self._get_class(arg, self.default_path)
    def __init__(self, class_to_wrap: Optional[type] = None, path: Optional[str] = None):
        self.default_path = path
        SaveableObject.__init__(self, None)