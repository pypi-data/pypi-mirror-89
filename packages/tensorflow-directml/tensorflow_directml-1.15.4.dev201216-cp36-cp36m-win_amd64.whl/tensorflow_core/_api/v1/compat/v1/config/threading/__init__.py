# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.config.threading namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.framework.config import get_inter_op_parallelism_threads
from tensorflow.python.framework.config import get_intra_op_parallelism_threads
from tensorflow.python.framework.config import set_inter_op_parallelism_threads
from tensorflow.python.framework.config import set_intra_op_parallelism_threads

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.config.threading", public_apis=None, deprecation=False,
      has_lite=False)
