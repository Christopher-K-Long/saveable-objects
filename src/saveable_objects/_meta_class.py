import inspect

class SaveAfterInitMetaClass(type):
    """A metaclass that saves object to the specified path after initialization.
    """
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        bound_args = inspect.signature(cls.__init__).bind(..., *args, **kwargs)
        bound_args.apply_defaults()
        path = bound_args.arguments["path"]
        if path is None:
            if hasattr(obj, "_path"):
                path = obj._path
        obj.path = path
        if obj.path is not None:
            obj.path = path
            obj._save(obj.path)
        return obj