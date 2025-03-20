# Getting Started

## What is saveable-objects

A SaveableObject is a wrapper around [pickle](https://docs.python.org/3/library/pickle.html) that allows the state of a python object to easily be saved and reloaded. This makes for easy checkpointing and is especially useful for scientific computing.

The idea of the package is to integrate checkpointing and saving as unintrusively into your python work as possible.

## Installation

The python package can be installed with pip as follows:
```bash
pip install saveable-objects
```

## Quick Start

Suppose we have the following simple script for adding two numbers and storing the result:
```python
class A():
    def __init__(self, x, y):
        self.result = x+y

a = A(1,2)


print(a.result)
```
```bash
3
```

We can modify this code to save ``a`` to the file ``a.pkl`` and then load ``a.pkl`` into a variable ``b`` as follows:
```python
from saveable_objects.extensions import SaveableWrapper

class A():
    def __init__(self, x, y):
        self.result = x+y

SaveableA = SaveableWrapper[A]; # Constructs a saveable version of the class A

a = SaveableA(1,2, path="a.pkl")
b = SaveableA.load("a.pkl")

print(a.result)
print(b.result)

```
```bash
3
3
```

We can also go on to update ``a`` and save it as follows:
```python
a.result = 4
a.save() # Overwrite a.pkl

a.result = 5
a.save("a_new.pkl")

print(SaveableA.load("a.pkl").result)
print(SaveableA.load("a_new.pkl").result)
```
```bash
4
5
```

Now you are ready to start saving and loading objects. Next we will look at creating your own [``SaveableObject``](../reference/_autosummary/saveable_objects.SaveableObject.rst)s

---

[Previous](overview.md) | [Next](creating_a_saveableobject.md)