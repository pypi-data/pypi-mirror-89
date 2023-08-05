# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""`tf.data.Dataset` API for input pipelines.

See [Importing Data](https://tensorflow.org/guide/datasets) for an overview.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.compat.v1.data import experimental
from tensorflow.python.data.ops.dataset_ops import Dataset
from tensorflow.python.data.ops.dataset_ops import DatasetSpec
from tensorflow.python.data.ops.dataset_ops import Options
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_classes as get_output_classes
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_shapes as get_output_shapes
from tensorflow.python.data.ops.dataset_ops import get_legacy_output_types as get_output_types
from tensorflow.python.data.ops.dataset_ops import make_initializable_iterator
from tensorflow.python.data.ops.dataset_ops import make_one_shot_iterator
from tensorflow.python.data.ops.iterator_ops import Iterator
from tensorflow.python.data.ops.readers import FixedLengthRecordDataset
from tensorflow.python.data.ops.readers import TFRecordDataset
from tensorflow.python.data.ops.readers import TextLineDataset

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.data", public_apis=None, deprecation=False,
      has_lite=False)
