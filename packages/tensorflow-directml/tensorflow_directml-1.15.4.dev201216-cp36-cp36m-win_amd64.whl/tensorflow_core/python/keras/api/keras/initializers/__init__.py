# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Keras initializer serialization / deserialization.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.initializers import RandomNormal
from tensorflow.python.keras.initializers import RandomNormal as normal
from tensorflow.python.keras.initializers import RandomNormal as random_normal
from tensorflow.python.keras.initializers import RandomUniform
from tensorflow.python.keras.initializers import RandomUniform as random_uniform
from tensorflow.python.keras.initializers import RandomUniform as uniform
from tensorflow.python.keras.initializers import TruncatedNormal
from tensorflow.python.keras.initializers import TruncatedNormal as truncated_normal
from tensorflow.python.keras.initializers import deserialize
from tensorflow.python.keras.initializers import get
from tensorflow.python.keras.initializers import serialize
from tensorflow.python.ops.init_ops import Constant
from tensorflow.python.ops.init_ops import Constant as constant
from tensorflow.python.ops.init_ops import GlorotNormal as glorot_normal
from tensorflow.python.ops.init_ops import GlorotUniform as glorot_uniform
from tensorflow.python.ops.init_ops import Identity
from tensorflow.python.ops.init_ops import Identity as identity
from tensorflow.python.ops.init_ops import Initializer
from tensorflow.python.ops.init_ops import Ones
from tensorflow.python.ops.init_ops import Ones as ones
from tensorflow.python.ops.init_ops import Orthogonal
from tensorflow.python.ops.init_ops import Orthogonal as orthogonal
from tensorflow.python.ops.init_ops import VarianceScaling
from tensorflow.python.ops.init_ops import Zeros
from tensorflow.python.ops.init_ops import Zeros as zeros
from tensorflow.python.ops.init_ops import he_normal
from tensorflow.python.ops.init_ops import he_uniform
from tensorflow.python.ops.init_ops import lecun_normal
from tensorflow.python.ops.init_ops import lecun_uniform

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.initializers", public_apis=None, deprecation=True,
      has_lite=False)
