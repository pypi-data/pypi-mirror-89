# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.lookup namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.lookup import experimental
from tensorflow.python.ops.lookup_ops import KeyValueTensorInitializer
from tensorflow.python.ops.lookup_ops import StaticHashTableV1 as StaticHashTable
from tensorflow.python.ops.lookup_ops import StaticVocabularyTableV1 as StaticVocabularyTable
from tensorflow.python.ops.lookup_ops import TextFileIndex
from tensorflow.python.ops.lookup_ops import TextFileInitializer

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "lookup", public_apis=None, deprecation=True,
      has_lite=False)
