# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Built-in activation functions.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.activations import deserialize
from tensorflow.python.keras.activations import elu
from tensorflow.python.keras.activations import exponential
from tensorflow.python.keras.activations import get
from tensorflow.python.keras.activations import hard_sigmoid
from tensorflow.python.keras.activations import linear
from tensorflow.python.keras.activations import relu
from tensorflow.python.keras.activations import selu
from tensorflow.python.keras.activations import serialize
from tensorflow.python.keras.activations import sigmoid
from tensorflow.python.keras.activations import softmax
from tensorflow.python.keras.activations import softplus
from tensorflow.python.keras.activations import softsign
from tensorflow.python.keras.activations import tanh

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.activations", public_apis=None, deprecation=True,
      has_lite=False)
