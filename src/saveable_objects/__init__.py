"""
A python package for checkpointing, saving, and loading objects.
"""

import sys

if sys.version_info[1] >= 10: # check if python is version 3.8 or later
    from ._saveable_object import SaveableObject
else: # import from the python version 3.7 compatable file
    from ._saveable_object_3_7 import SaveableObject