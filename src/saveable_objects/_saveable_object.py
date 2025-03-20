import os
import inspect
import numpy as np
import pickle as pkl
import cloudpickle as cpkl
from typing import Optional, Literal, IO, Tuple

from ._meta_class import SaveAfterInitMetaClass

class SaveableObject(metaclass=SaveAfterInitMetaClass):
    """A utility class for saving objects to pickles and checkpointing.
    """
    def __init__(self, path: Optional[str] = None):
        """Initialises an instance of the :class:`SaveableObject`.
        If a path is specified the saveable object is automatically saved after
        initialisation.

        Parameters
        ----------
        path : str, optional
            The file :attr:`path` to save the object to. If ``None`` then the
            object is not saved. By default ``None``.

        Notes
        -----
        If no file extension is provided for `path` then the class name and the
        ``.pkl`` extension are appended to the file name.
        """
        self.path = path
    @property
    def path(self) -> Optional[str]:
        """The current file path of the object.

        Notes
        -----
        On setting the value, if no file extension is provided then the class
        name and the ``.pkl`` extension are appended to the file name.
        """
        return self._path
    @path.setter
    def path(self, value: Optional[str]):
        """Set the current file path of the object.

        Parameters
        ----------
        value : str, optional
            The new file path of the object. By default ``None``.

        Notes
        -----
        If no file extension is provided then the class name and the ``.pkl``
        extension are appended to the file name.
        """
        self._path = self._updatepathroot(value)
    @classmethod
    def _get_name(cls, path: Optional[str]) -> Optional[str]:
        """Returns the file name of the specified path (without the file
        extension).

        Parameters
        ----------
        path : str, optional
            The path to obtain the file name for.

        Returns
        -------
        str, optional
            The file name (without the file extension).
        """
        if path is None:
            return None
        return os.path.split(os.path.splitext(cls._updatepathroot(path))[0])[-1]
    @property
    def name(self) -> Optional[str]:
        """The file name of the object (without the file extension). Note that
        `name` is read only.
        """
        return self._get_name(self._path)
        
    def _save(self, path: str, write_mode: Literal["w", "wb", "a", "ab", "x", "xb"] = "wb"):
        """Saves the object to `path` using `write_mode`.

        Parameters
        ----------
        path : str
            The path to save the object to.
        write_mode : Literal["w", "wb", "a", "ab", "x", "xb"], optional
            The mode with which to open the file to write to. These are the same
            as `mode` for ``open``. By default ``"wb"``.
        """
        if not os.path.exists(path):
            if (dirname := os.path.dirname(path)) != '':
                os.makedirs(dirname, exist_ok=True)
        with open(path, write_mode) as file:
            cpkl.dump(self, file, pkl.HIGHEST_PROTOCOL)
    def _getpath(self, path: Optional[str]) -> str:
        """Returns the specified or saved :attr:`path`.

        Parameters
        ----------
        path : str, optional
            Specified path.

        Returns
        -------
        str
            Returns the specified or saved :attr:`path`.

        Raises
        ------
        ValueError
            No save path provided. Raised if no path is saved or specified.
        """
        path = path if path is not None or not hasattr(self, 'path') else self.path
        if path is None:
            raise ValueError("No save path provided.")
        path = self._updatepathroot(path)
        return path
    @classmethod
    def _updatepathroot(cls, path: Optional[str]) -> Optional[str]:
        """If no file extension is provided then the class name and the ``.pkl``
        extension are appended to the file name.

        Parameters
        ----------
        path : str, optional
            The file path.

        Returns
        -------
        str, optional
            The modified file path.
        """
        if path is None:
            return None
        split = os.path.splitext(path)
        if len(split[1]) == 0:
            file_name = os.path.split(split[0])[-1]
            prefix = "_" if len(file_name) != 0 and file_name[-1] != "_" else ""
            path += prefix + cls.__name__ + ".pkl"
        return path
    def save(self, path: Optional[str] = None):
        """Pickles the current instance.

        Parameters
        ----------
        path : str, optional
            The path to pickle the instance to. If ``None`` is specified
            then the attribute :attr:`path` is used instead.
            By default ``None``.

        Raises
        ------
        ValueError
            Raised if no path specified either by the parameter `path` or the
            attribute :attr:`path`.

        Notes
        -----
        If no file extension is provided then the class name and the ``.pkl``
        extension are appended to the file name.
        """
        self.path = self._getpath(path)
        self._save(self.path)
    def update_save(self, path: Optional[str] = None) -> bool:
        """Pickles the current instance and retains the saved arguments if
        they exist.

        Parameters
        ----------
        path : str, optional
            The path to pickle the instance to. If ``None`` is specified
            then the attribute :attr:`path` is used instead. By default
            ``None``.

        Returns
        -------
        bool
            ``True`` if there was an argument pickle to retain. ``False`` if
            there was not an argument pickle to retain.

        Raises
        ------
        ValueError
            Raised if no path specified.

        Notes
        -----
        If no file extension is provided then the class name and the ``.pkl``
        extension are appended to the file name.
        """
        self.path = self._getpath(path)
        file = open(self.path, "rb")
        # Throw away the prior save:
        try:
            type(self)._load(file)
        except:
            pass
        # Retain the parameters:
        try:
            params = pkl.load(file)
        except EOFError:
            # Close the file before writing to it
            file.close()
            self._save(self.path)
            return False
        else:
            # Close the file before writing to it
            file.close()
            self._save(self.path)
            SaveableObject._save(params, self.path, write_mode="ab")
            return True
        
    @classmethod
    def _load(cls, file: IO, new_path: Optional[str] = None, strict_typing: bool = True) -> "SaveableObject":
        """Loads an instance from the `file`.

        Parameters
        ----------
        file : IO
            The file to load the instance from.
        new_path : str, optional
            The path to replace the previous path with. If ``None`` the `path`
            is not replaced. By default ``None``.
        strict_typing : bool, optional
            If ``True`` then the loaded instance must be an instance of `cls`.
            By default ``True``.

        Returns
        -------
        `cls`
            The loaded instance.

        Raises
        ------
        TypeError
            If `strict_typing` and the loaded instance is not an instance of
            `cls`.

        Notes
        -----
        ``strict_typing=True`` acts as a safety guard. Setting
        ``strict_typing=False`` may increase the probability of unexpected or
        uncaught errors.
        """
        instance =  pkl.load(file)
        if strict_typing and not isinstance(instance, cls):
            raise TypeError(f"The loaded instance is not an instance of {cls}.")
        if new_path is not None:
            instance.path = new_path
        return instance
    @classmethod
    def load(cls, path: str, new_path: Optional[str] = None, strict_typing: bool = True) -> "SaveableObject":
        """Loads a pickled instance.

        Parameters
        ----------
        path : str
            The path of the pickle.
        new_path : str, optional
            The path to replace the previous path with. If ``None`` the `path`
            is not replaced. By default ``None``.
        strict_typing : bool, optional
            If ``True`` then the loaded instance must be an instance of `cls`.
            By default ``True``.

        Returns
        -------
        SaveableObject
            The loaded instance.

        Raises
        ------
        TypeError
            If `strict_typing` and the loaded instance is not an instance of
            `cls`.

        Notes
        -----
        ``strict_typing=True`` acts as a safety guard. Setting
        ``strict_typing=False`` may increase the probability of unexpected or
        uncaught errors.
        """
        path = cls._updatepathroot(path)
        with open(path, "rb") as file:
            return cls._load(file, new_path, strict_typing)
    @classmethod
    def tryload(cls, path: Optional[str], new_path: Optional[str] = None, strict_typing: bool = True) -> "SaveableObject" | Literal[False]:
        """Attempts to :meth:`load` from the specified `path`. If the loading
        fails then ``False`` is returned.

        Parameters
        ----------
        path : str, optional
            The path of the pickle. If ``None`` then ``False`` is returned.
        new_path : str, optional
            The path to replace the previous path with. If ``None`` the `path`
            is not replaced. By default ``None``.
        strict_typing : bool, optional
            If ``True`` then the loaded instance must be an instance of `cls`.
            By default ``True``.

        Returns
        -------
        SaveableObject | Literal[False]
            If succeeded the loaded instance, else False.

        Notes
        -----
        ``strict_typing=True`` acts as a safety guard. Setting
        ``strict_typing=False`` may increase the probability of unexpected or
        uncaught errors.
        """
        try:
            return cls.load(path, new_path, strict_typing)
        except (FileNotFoundError, TypeError):
            return False
    @classmethod
    def loadif(cls, *args, **kwargs) -> Tuple["SaveableObject", bool]:
        """Attempts to load from a specified `path`. If the loading fails or no
        `path` is specified then a new instance of the object is generated with
        the specified `*args` and `**kwargs`.

        Parameters
        ----------
        *args
            The arguments to pass to the initialisation on a failed
            :meth:`load`.
        path : str, optional
            The path of the pickle, by default the parameter is not specified.
        **kwargs
            The keyword arguments to pass to the initialisation on a failed
            :meth:`load`.
        
        Returns
        -------
        (SaveableObject, bool)
            The loaded or initialised instance followed by ``True`` if the
            instance was loaded and ``False`` if the instance was initialised.
        """
        bound_args = inspect.signature(cls.__init__).bind(..., *args, **kwargs)
        try:
            path = bound_args.arguments["path"]
        except KeyError:
            path = None
        if instance := cls.tryload(path):
            return instance, True
        return cls(*args, **kwargs), False
    @classmethod
    def loadifparams(cls, *args, dependencies: dict = {}, **kwargs) -> Tuple["SaveableObject", bool]:
        """Attempts to :meth:`load` from a specified `path`. If the loading
        fails or no `path` is specified or the parameters do not match the saved
        parameters then a new instance of the object is generated with the
        specified `*args` and `**kwargs`.

        Parameters
        ----------
        *args
            The arguments to pass to the initialisation on a failed
            :meth:`load`.
        path : str, optional
            The path of the pickle, by default the parameter is not specified.
        dependencies : dict, optional, must be specified as a keyword argument
            A dictionary of additional dependencies to check.
        **kwargs
            The keyword arguments to pass to the initialisation on a failed
            :meth:`load`.
        
        Returns
        -------
        (SaveableObject, bool)
            The loaded or initialised instance followed by ``True`` if the
            instance was loaded and ``False`` if the instance was initialised.
        """
        bound_args = inspect.signature(cls.__init__).bind(..., *args, **kwargs)
        try:
            path = bound_args.arguments["path"]
        except KeyError:
            path = None
        path = cls._updatepathroot(path)
        duplicates = []
        for key in dependencies.keys():
            if key in bound_args.arguments.keys():
                duplicates.append(key)
        if len(duplicates) != 0:
            raise TypeError(f"The dependencies {duplicates} are also arguments. They must have different names.")
        arguments = {**bound_args.arguments, **dependencies}
        try:
            with open(path, "rb") as file:
                instance = cls._load(file)
                params = pkl.load(file)
            for key, value in arguments.items():
                comparison = params[key] != value
                if isinstance(comparison, bool):
                    if comparison:
                        raise ValueError
                else:
                    if not np.array_equal(params[key], value):
                        raise ValueError
            return instance, True
        except (FileNotFoundError, EOFError, ValueError, TypeError, KeyError):
            instance = cls(*args, **kwargs)
            if path is not None:
                SaveableObject._save(arguments, path, write_mode="ab")
            return instance, False