# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""NASNet-A models for Keras.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.applications import NASNetLarge
from tensorflow.python.keras.applications import NASNetMobile
from tensorflow.python.keras.applications.nasnet import decode_predictions
from tensorflow.python.keras.applications.nasnet import preprocess_input

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.applications.nasnet", public_apis=None, deprecation=False,
      has_lite=False)
