# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Confusion matrix related metrics."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.ops import confusion_matrix as cm


def confusion_matrix(labels, predictions, num_classes=None, dtype=dtypes.int32,
                     name=None, weights=None):
  """Deprecated. Use tf.math.confusion_matrix instead."""
  return cm.confusion_matrix(labels=labels, predictions=predictions,
                             num_classes=num_classes, dtype=dtype, name=name,
                             weights=weights)
