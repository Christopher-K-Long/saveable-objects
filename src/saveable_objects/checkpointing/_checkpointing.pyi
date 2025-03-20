from typing import Tuple

from .._saveable_object import SaveableObject

def failed(load_attempt: SaveableObject | bool | Tuple[SaveableObject, bool]) -> bool:
    """Determines if a ``SaveableObject`` ``.load()``, ``.tryload()``,
    ``.loadif()``, or ``.loadifparams()`` attempt fails.

    Parameters
    ----------
    load_attempt : SaveableObject | bool | (SaveableObject, bool)
        The output of ``load()``, ``tryload()``, ``loadif()``, or
        ``loadifparams()``.

    Returns
    -------
    bool
        Returns ``True`` is the the `load_attempt` failed, else ``False``.

    Notes
    -----
    Example use:

    .. code-block:: python
    
        if failed(obj := SaveableObject.loadif(*args, path="filename.pkl", **kwargs)):
            ... # code that generates obj
        ... # code that uses obj
    """

def succeeded(load_attempt: SaveableObject | bool | Tuple[SaveableObject, bool]) -> bool:
    """Determines if a ``SaveableObject`` ``.load()``, ``.tryload()``,
    ``.loadif()``, or ``.loadifparams()`` attempt succeeds.

    Parameters
    ----------
    load_attempt : SaveableObject | bool | (SaveableObject, bool)
        The output of ``load()``, ``tryload()``, ``loadif()``, or
        ``loadifparams()``.

    Returns
    -------
    bool
        Returns ``True`` is the the `load_attempt` succeeded, else ``False``.

    Notes
    -----
    Example use:

    .. code-block:: python
    
        if succeeded(obj := SaveableObject.loadif(*args, path="filename.pkl", **kwargs)):
            ... # code that uses a successfully loaded obj
        else:
            ... # code to run if obj failed to load
    """