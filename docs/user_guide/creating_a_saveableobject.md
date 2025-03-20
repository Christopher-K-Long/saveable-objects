# Creating a SaveableObject

At the heart of saveable-objects lies the class [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst). There are several ways to create a [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst)s which we will outline here:
1. [Inheritance](#inheritance)
2. [Decorating](#decorating)
3. [Wrapping](#wrapping)

Throughout this tutorial we will consider converting the class
```python
class A():
    pass
```
to a saveable-object.

## Inheritance

You can design a class to be a saveable-object from the ground up via inheritance. To achieve this you **must** do two things:
1. Inherit [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst)
2. Add ``path`` as a keyword arguement to the ``__init__`` function:

For example,
```python
from saveable_objects import SaveableObject

class A(SaveableObject):
    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
```

Note if you forget step 2., i.e.,
For example,
```python
from saveable_objects import SaveableObject

class A(SaveableObject):
    def __init__(self):
        super().__init__("fixed_path.pkl")
```
the code will crash. This is because the path variable is intercepted from 

## Decorating

A less intrusive but less transparent method is to decorate the definition of ``A`` with [``SaveableWrapper``](../reference/_autosummary/saveable_objects.extensions.SaveableWrapper.rst):

```python
from saveable_objects.extensions import SaveableWrapper

@SaveableWrapper
class A():
    pass
```

We can also pass a default path as follows:
```python
from saveable_objects.extensions import SaveableWrapper

@SaveableWrapper(path="default_path.pkl")
class A():
    pass
```

Note that under the hood this will result in a slightly different inheritance structure than achieved via the [inheritance](#inheritance) method. Specifically the decorator generates a new class that will be called ``A`` that inherits the old ``A`` and [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst).

## Wrapping

Sometimes you might import ``A`` from a package or other code you don't wish to modify. A consise solution to this is to wrap the class ``A`` using [``SaveableWrapper``](../reference/_autosummary/saveable_objects.extensions.SaveableWrapper.rst):

```python
from saveable_objects.extensions import SaveableWrapper

A = SaveableWrapper[A];
```

We can also pass a default path as follows:
```python
from saveable_objects.extensions import SaveableWrapper

A = SaveableWrapper(path="default_path.pkl")[A];
```

Note, just as with [decoration](#decorating) method, under the hood this will result in a slightly different inheritance structure than achieved via the [Inheritance](#inheritance) method. Specifically the decorator generates a new class that will be called ``A`` that inherits the old ``A`` and [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst).

---
[Previous](getting_started.md) | [Next](saving_and_loading.md)