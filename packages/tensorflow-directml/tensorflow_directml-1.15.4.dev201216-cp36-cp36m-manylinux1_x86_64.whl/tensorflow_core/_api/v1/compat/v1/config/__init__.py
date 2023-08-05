# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.config namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.compat.v1.config import experimental
from tensorflow._api.v1.compat.v1.config import optimizer
from tensorflow._api.v1.compat.v1.config import threading
from tensorflow.python.eager.context import list_devices as experimental_list_devices
from tensorflow.python.eager.def_function import run_functions_eagerly as experimental_run_functions_eagerly
from tensorflow.python.eager.remote import connect_to_cluster as experimental_connect_to_cluster
from tensorflow.python.eager.remote import connect_to_remote_host as experimental_connect_to_host
from tensorflow.python.framework.config import get_soft_device_placement
from tensorflow.python.framework.config import set_soft_device_placement

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.config", public_apis=None, deprecation=False,
      has_lite=False)
