# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""System configuration library.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.framework.versions import CXX11_ABI_FLAG
from tensorflow.python.framework.versions import MONOLITHIC_BUILD
from tensorflow.python.platform.sysconfig import get_compile_flags
from tensorflow.python.platform.sysconfig import get_include
from tensorflow.python.platform.sysconfig import get_lib
from tensorflow.python.platform.sysconfig import get_link_flags

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.sysconfig", public_apis=None, deprecation=False,
      has_lite=False)
