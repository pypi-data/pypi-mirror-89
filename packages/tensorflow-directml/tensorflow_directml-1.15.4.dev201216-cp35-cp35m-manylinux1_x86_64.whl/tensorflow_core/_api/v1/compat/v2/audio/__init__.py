# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.audio namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.gen_audio_ops import decode_wav
from tensorflow.python.ops.gen_audio_ops import encode_wav

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v2.audio", public_apis=None, deprecation=False,
      has_lite=False)
