# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""SavedModel utility functions.

Utility functions to assist with setup and construction of the SavedModel proto.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.saved_model.utils_impl import build_tensor_info
from tensorflow.python.saved_model.utils_impl import get_tensor_from_tensor_info

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "saved_model.utils", public_apis=None, deprecation=True,
      has_lite=False)
