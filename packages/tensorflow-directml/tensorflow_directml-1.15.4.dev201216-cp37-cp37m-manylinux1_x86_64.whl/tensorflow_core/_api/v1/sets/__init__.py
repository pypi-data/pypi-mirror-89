# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Tensorflow set operations.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.sets_impl import set_difference
from tensorflow.python.ops.sets_impl import set_difference as difference
from tensorflow.python.ops.sets_impl import set_intersection
from tensorflow.python.ops.sets_impl import set_intersection as intersection
from tensorflow.python.ops.sets_impl import set_size
from tensorflow.python.ops.sets_impl import set_size as size
from tensorflow.python.ops.sets_impl import set_union
from tensorflow.python.ops.sets_impl import set_union as union

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "sets", public_apis=None, deprecation=True,
      has_lite=False)
