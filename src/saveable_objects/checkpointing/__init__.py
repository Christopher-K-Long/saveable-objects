"""
A collection of functions for checkpointing objects.
"""

import sys

if sys.version_info[1] >= 10: # check if python is version 3.8 or later
    from ._checkpointing import failed, succeeded
else: # import from the python version 3.7 compatable file
    from ._checkpointing_3_7 import failed, succeeded