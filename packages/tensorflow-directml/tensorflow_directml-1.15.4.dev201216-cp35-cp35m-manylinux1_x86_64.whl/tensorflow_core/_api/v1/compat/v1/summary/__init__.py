# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Operations for writing summary data, for use in analysis and visualization.

See the [Summaries and
TensorBoard](https://www.tensorflow.org/guide/summaries_and_tensorboard) guide.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python import Event
from tensorflow.python import SessionLog
from tensorflow.python import Summary
from tensorflow.python import SummaryDescription
from tensorflow.python import TaggedRunMetadata
from tensorflow.python.ops.summary_ops_v2 import all_v2_summary_ops
from tensorflow.python.ops.summary_ops_v2 import initialize
from tensorflow.python.summary.summary import audio
from tensorflow.python.summary.summary import get_summary_description
from tensorflow.python.summary.summary import histogram
from tensorflow.python.summary.summary import image
from tensorflow.python.summary.summary import merge
from tensorflow.python.summary.summary import merge_all
from tensorflow.python.summary.summary import scalar
from tensorflow.python.summary.summary import tensor_summary
from tensorflow.python.summary.summary import text
from tensorflow.python.summary.writer.writer import FileWriter
from tensorflow.python.summary.writer.writer_cache import FileWriterCache

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.summary", public_apis=None, deprecation=False,
      has_lite=False)
