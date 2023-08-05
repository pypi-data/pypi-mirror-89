# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""SignatureDef utility functions.

Utility functions for building and inspecting SignatureDef protos.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def
from tensorflow.python.saved_model.signature_def_utils_impl import classification_signature_def
from tensorflow.python.saved_model.signature_def_utils_impl import is_valid_signature
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
from tensorflow.python.saved_model.signature_def_utils_impl import regression_signature_def

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.saved_model.signature_def_utils", public_apis=None, deprecation=False,
      has_lite=False)
