# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Evaluation-related metrics.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.metrics_impl import accuracy
from tensorflow.python.ops.metrics_impl import auc
from tensorflow.python.ops.metrics_impl import average_precision_at_k
from tensorflow.python.ops.metrics_impl import false_negatives
from tensorflow.python.ops.metrics_impl import false_negatives_at_thresholds
from tensorflow.python.ops.metrics_impl import false_positives
from tensorflow.python.ops.metrics_impl import false_positives_at_thresholds
from tensorflow.python.ops.metrics_impl import mean
from tensorflow.python.ops.metrics_impl import mean_absolute_error
from tensorflow.python.ops.metrics_impl import mean_cosine_distance
from tensorflow.python.ops.metrics_impl import mean_iou
from tensorflow.python.ops.metrics_impl import mean_per_class_accuracy
from tensorflow.python.ops.metrics_impl import mean_relative_error
from tensorflow.python.ops.metrics_impl import mean_squared_error
from tensorflow.python.ops.metrics_impl import mean_tensor
from tensorflow.python.ops.metrics_impl import percentage_below
from tensorflow.python.ops.metrics_impl import precision
from tensorflow.python.ops.metrics_impl import precision_at_k
from tensorflow.python.ops.metrics_impl import precision_at_thresholds
from tensorflow.python.ops.metrics_impl import precision_at_top_k
from tensorflow.python.ops.metrics_impl import recall
from tensorflow.python.ops.metrics_impl import recall_at_k
from tensorflow.python.ops.metrics_impl import recall_at_thresholds
from tensorflow.python.ops.metrics_impl import recall_at_top_k
from tensorflow.python.ops.metrics_impl import root_mean_squared_error
from tensorflow.python.ops.metrics_impl import sensitivity_at_specificity
from tensorflow.python.ops.metrics_impl import sparse_average_precision_at_k
from tensorflow.python.ops.metrics_impl import sparse_precision_at_k
from tensorflow.python.ops.metrics_impl import specificity_at_sensitivity
from tensorflow.python.ops.metrics_impl import true_negatives
from tensorflow.python.ops.metrics_impl import true_negatives_at_thresholds
from tensorflow.python.ops.metrics_impl import true_positives
from tensorflow.python.ops.metrics_impl import true_positives_at_thresholds

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.metrics", public_apis=None, deprecation=False,
      has_lite=False)
