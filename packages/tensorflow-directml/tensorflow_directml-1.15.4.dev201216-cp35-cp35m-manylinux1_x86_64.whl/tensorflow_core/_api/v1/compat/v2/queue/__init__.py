# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.queue namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.data_flow_ops import FIFOQueue
from tensorflow.python.ops.data_flow_ops import PaddingFIFOQueue
from tensorflow.python.ops.data_flow_ops import PriorityQueue
from tensorflow.python.ops.data_flow_ops import QueueBase
from tensorflow.python.ops.data_flow_ops import RandomShuffleQueue

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v2.queue", public_apis=None, deprecation=False,
      has_lite=False)
