# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.initializers namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.init_ops import Constant as constant
from tensorflow.python.ops.init_ops import GlorotNormal as glorot_normal
from tensorflow.python.ops.init_ops import GlorotUniform as glorot_uniform
from tensorflow.python.ops.init_ops import Identity as identity
from tensorflow.python.ops.init_ops import Ones as ones
from tensorflow.python.ops.init_ops import Orthogonal as orthogonal
from tensorflow.python.ops.init_ops import RandomNormal as random_normal
from tensorflow.python.ops.init_ops import RandomUniform as random_uniform
from tensorflow.python.ops.init_ops import TruncatedNormal as truncated_normal
from tensorflow.python.ops.init_ops import UniformUnitScaling as uniform_unit_scaling
from tensorflow.python.ops.init_ops import VarianceScaling as variance_scaling
from tensorflow.python.ops.init_ops import Zeros as zeros
from tensorflow.python.ops.init_ops import he_normal
from tensorflow.python.ops.init_ops import he_uniform
from tensorflow.python.ops.init_ops import lecun_normal
from tensorflow.python.ops.init_ops import lecun_uniform
from tensorflow.python.ops.lookup_ops import tables_initializer
from tensorflow.python.ops.variables import global_variables_initializer as global_variables
from tensorflow.python.ops.variables import local_variables_initializer as local_variables
from tensorflow.python.ops.variables import variables_initializer as variables

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.initializers", public_apis=None, deprecation=False,
      has_lite=False)
