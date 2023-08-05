# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Conversion of plain Python into TensorFlow graph code.

NOTE: In TensorFlow 2.0, AutoGraph is automatically applied when using
`tf.function`. This module contains lower-level APIs for advanced use.

For more information, see the
[AutoGraph guide](https://www.tensorflow.org/guide/autograph).

By equivalent graph code we mean code that generates a TensorFlow graph when
run. The generated graph has the same effects as the original code when executed
(for example with `tf.function` or `tf.compat.v1.Session.run`). In other words,
using AutoGraph can be thought of as running Python in TensorFlow.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.autograph import experimental
from tensorflow.python.autograph.impl.api import to_code_v1 as to_code
from tensorflow.python.autograph.impl.api import to_graph_v1 as to_graph
from tensorflow.python.autograph.utils.ag_logging import set_verbosity
from tensorflow.python.autograph.utils.ag_logging import trace

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "autograph", public_apis=None, deprecation=True,
      has_lite=False)
