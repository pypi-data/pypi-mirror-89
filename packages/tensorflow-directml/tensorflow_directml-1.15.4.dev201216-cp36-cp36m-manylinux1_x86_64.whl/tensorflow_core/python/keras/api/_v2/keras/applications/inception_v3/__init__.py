# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Inception V3 model for Keras.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.applications import InceptionV3
from tensorflow.python.keras.applications.inception_v3 import decode_predictions
from tensorflow.python.keras.applications.inception_v3 import preprocess_input

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.applications.inception_v3", public_apis=None, deprecation=False,
      has_lite=False)
