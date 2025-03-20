# Saving and loading

Now we can create saveable-objects we can start saving a loading them. First we will consider saving.

## Saving

When we create a new instance of an object we can choose whether to save the instance immediately after initialisation by including the ``path`` keyword argument
```python
a = SaveableObject(path="a.pkl")
```
or not
```python
a = SaveableObject()
```
Note that path **must** only be passed as a keyword argument and never as a positional argument.

We can also choose to save an object at any later time with [``.save()``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.save). For example,
```python
a = SaveableObject()
a.save("a.pkl")
```
is equivalent to
```python
a = SaveableObject(path="a.pkl")
```

When ever we save an object ``a`` to a given ``path`` the attribute ``a.path`` is set to ``path``. Consider the following example:
```python
a = SaveableObject(path="a.pkl")
a.x = 1
a.save() # overwrites the file a.pkl with the new state of a
a.x = 2
a.save(path="b.pkl") # writes to a different file b.pkl with the new state of a
a.x = 3
a.save() # overwrites the file b.pkl with the new state of a
```

Finally, if we save to a path ``folder/a.pkl`` the directory ``folder`` will be created if it does not yet exist.

## Loading

There are several ways to load a [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst). The simplest is [``.load()``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.load):
```python
a = SaveableObject.load("a.pkl")
```

When we load an object we can choose to update the attribute ``.path`` to a new value. This will help prevent us overwriting the old file when we save again
```python
a = SaveableObject.load("a.pkl", "new_filename.pkl") # this will load from "a.pkl"
a.save() # this will save to "new_filename.pkl"
```

We also need to be careful about what class we are planning to load. By default saveable-objects employs strict typing when loading [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst)s. That is
```python
from saveable_objects.extensions import SaveableWrapper

@SaveableWrapper
class A(): pass
class B(A): pass
b = B(path="instance_of_B.pkl")
A.load("instance_of_B.pkl")
```
run as ``A`` is not a child class of ``B``. But
```python
a = A(path="instance_of_A.pkl")
B.load("instance_of_A.pkl")
```
will raise a ``TypeError`` if ``B`` is a child class of ``A``. We can disable this feature with the ``strict_typing`` parameter:
```python
B.load("instance_of_A.pkl", strict_typing=False)
```

### Attempting to load

It may be the case we don't know if the file ``a.pkl`` exists. If it does not and we run [``SaveableObject.load("a.pkl")``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.load) an error will be raised. to remove the hassle of handelling such errors we can use [``tryload``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.tryload). [``tryload``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.tryload) returns the loaded object if no errors arise or ``False`` if an error did arise. Coupled with the walrus operator ``:=`` this allows us to write flows as follows:
```python
if(a := SaveableObject.tryload("a.pkl")):
    # a.pkl exists so we can now go an use it
    print(a)
else:
    # a.pkl does not exist and the variable a is set to False. So here we could, for example, generate a:
    a = SaveableObject("a.pkl")
    print(a)
```

This flow can be made more readable with the utility functions [``succeeded``](../reference/_autosummary/saveable_objects.checkpointing.succeeded.rst) and [``failed``](../reference/_autosummary/saveable_objects.checkpointing.failed.rst):
```python
from saveable_objects.checkpointing import failed, succeeded
if succeeded(a := SaveableObject.tryload("a.pkl")):
    # a.pkl exists so we can now go an use it
    ...

if failed(a := SaveableObject.tryload("a.pkl")):
    # a.pkl does not exist and a is set to False
    ...
```

### Initialising when loading fails

It is commonly the case that if ``a.pkl`` does not exist we want to generate ``a.pkl``. For this task we can use [``loadif``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadif). [``loadif``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadif) loads ``a.pkl``, but if for some reason ``a.pkl`` cannot be loaded then it creates a new instance of ``a.pkl``. For example, consider the class:
```python
@SaveableWrapper
class A():
    def __init__(self, x, y):
        self.z = x+y
```
Suppose ``a.pkl`` does not exist. Then:
```python
A.loadif(1, 2, path="a.pkl")
```
is equivalent to
```python
A(1, 2, path="a.pkl")
```
which will save the generated instance of ``A`` to ``a.pkl``. However, if we run
```python
a, success = A.loadif(3, 4, path="a.pkl")
```
again, the code will be equivalent to
```python
a = A.load("a.pkl")
```
and we will find that ``a.z=1+2=3`` not ``a.z=3+4=7``. The ``success`` varible is a bool indicating whether the load was successful (``True``) or if the load failed and a new instance was initialised (``False``). As before we can use the utility functions [``succeeded``](../reference/_autosummary/saveable_objects.checkpointing.succeeded.rst) and [``failed``](../reference/_autosummary/saveable_objects.checkpointing.failed.rst):
```python
if succeeded((a, _ := A.loadif(1, 2, path="a.pkl"))):
    # a was loaded
    ...
else:
    # a was initialised
    ...

if failed((a, _ := A.loadif(1, 2, path="a.pkl"))):
    # a was initialised
    ...
else:
    # a was loaded
    ...
```

#### Different parameters

The odd thing in the last example was that even though we passed new parameters to [``loadif``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadif) we still loaded the old instance with the old parameters. Often this is not desirable behaviour. To fix this we can use [``loadifparams``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadifparams). Repeating the previous example:
```python
@SaveableWrapper
class A():
    def __init__(self, x, y):
        self.z = x+y
```
Once again, suppose ``a.pkl`` does not exist. Then:
```python
A.loadifparams(1, 2, path="a.pkl")
```
is equivalent to
```python
A(1, 2, path="a.pkl")
```
which will save the generated instance of ``A`` to ``a.pkl``. Similarly, if we run
```python
a, success = A.loadifparams(1, 2, path="a.pkl")
```
again, the code will be equivalent to
```python
a = A.load("a.pkl")
```
However, if we now run
```python
a, success = A.loadifparams(2, 1, path="a.pkl")
```
again, the code will be equivalent to
```python
a = A(2, 1, path="a.pkl")
```
That is [``loadifparams``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadifparams) checks if the file can be loaded and if so it checks the parameters used to initialise the instance are the same as before. If the parameters are different then a new instance is initialised which overwrites the old file. Notice it is the parameters that matter not the state as ``A(1, 2, path="a.pkl")`` and ``A(2, 1, path="a.pkl")`` have the same state (``z=3``).

The ``success`` varible, once again, is a bool indicating whether the instance was loaded (``True``) or or the instance was re-initialised (``False``). As before we can use the utility functions [``succeeded``](../reference/_autosummary/saveable_objects.checkpointing.succeeded.rst) and [``failed``](../reference/_autosummary/saveable_objects.checkpointing.failed.rst):
```python
if succeeded((a, _ := A.loadifparams(1, 2, path="a.pkl"))):
    # a was loaded
    ...
else:
    # a was initialised
    ...

if failed((a, _ := A.loadifparams(1, 2, path="a.pkl"))):
    # a was initialised
    ...
else:
    # a was loaded
    ...
```

#### Returning to saving

This now begs the question: How does [``loadifparams``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.loadifparams) know what the previous parameters were? Well under the hood two pickles are saved into the same file. The first pickle is the state of the object. The second pickle is the parameters used to initialise the object. This method means there is only a single file storing the data about the object **and** it's initial parameters. But it also mean such pickle files can still be opened by any other load function from saveable-objects, or [``pickle.load``](https://docs.python.org/3/library/pickle.html#pickle.load). This is because the load functions from saveable-objects and [``pickle.load``](https://docs.python.org/3/library/pickle.html#pickle.load) only load the first pickle from the file.

The downside to this approach is that if you want to update the instance and then save it again:
```python
a, _ = A.loadifparams(1, 2, path="a.pkl")
a.z = 10
a.save()
```
the final save will overwrite the saved parameters in the file ``a.pkl"``. This means that
```python
A.loadifparams(1, 2, path="a.pkl")
```
will now generate a new instance as the parameters no longer match.

This really is the desired behaviour because now the initialisation parameters do not accurately represent the steps taken to generate the current state of the object. Nonetheless, we can circumvent this behaviour with [``update_save``](../reference/_autosummary/saveable_objects.SaveableObject.rst#saveable_objects.SaveableObject.update_save). For example,
```python
a, _ = A.loadifparams(1, 2, path="a.pkl")
a.z = 10
a.update_save()
```
will not overwrite the parameters stored in ``a.pkl`` and so if we now run
```python
b, _ = A.loadifparams(1, 2, path="a.pkl")
```
we will this time load the state and find `b.z=10`.

---

This is the end of the tutorial. Now you know everything to use saveable-objects!

[Previous](creating_a_saveableobject.md)