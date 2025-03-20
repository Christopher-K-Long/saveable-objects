from typing import Tuple

from .._saveable_object import SaveableObject

def failed(load_attempt: SaveableObject | bool | Tuple[SaveableObject, bool]) -> bool:
    """Determines if a :class:`SaveableObject <saveable_objects.SaveableObject>`
    :meth:`.load() <saveable_objects.SaveableObject.load>`,
    :meth:`.tryload() <saveable_objects.SaveableObject.tryload>`,
    :meth:`.loadif() <saveable_objects.SaveableObject.loadif>`, or
    :meth:`.loadifparams() <saveable_objects.SaveableObject.loadifparams>` attempt
    fails.

    Parameters
    ----------
    load_attempt : SaveableObject | bool | (SaveableObject, bool)
        The output of :meth:`load() <saveable_objects.SaveableObject.load>`,
        :meth:`tryload() <saveable_objects.SaveableObject.tryload>`,
        :meth:`loadif() <saveable_objects.SaveableObject.loadif>`, or
        :meth:`loadifparams() <saveable_objects.SaveableObject.loadifparams>`.

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
    try:
        return not load_attempt[1]
    except:
        return not load_attempt
    
def succeeded(load_attempt: SaveableObject | bool | Tuple[SaveableObject, bool]) -> bool:
    """Determines if a :class:`SaveableObject <saveable_objects.SaveableObject>`
    :meth:`.load() <saveable_objects.SaveableObject.load>`,
    :meth:`.tryload() <saveable_objects.SaveableObject.tryload>`,
    :meth:`.loadif() <saveable_objects.SaveableObject.loadif>`, or
    :meth:`.loadifparams() <saveable_objects.SaveableObject.loadifparams>` attempt
    succeeds.

    Parameters
    ----------
    load_attempt : SaveableObject | bool | (SaveableObject, bool)
        The output of :meth:`load() <saveable_objects.SaveableObject.load>`,
        :meth:`tryload() <saveable_objects.SaveableObject.tryload>`,
        :meth:`loadif() <saveable_objects.SaveableObject.loadif>`, or
        :meth:`loadifparams() <saveable_objects.SaveableObject.loadifparams>`.

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
    return not failed(load_attempt)