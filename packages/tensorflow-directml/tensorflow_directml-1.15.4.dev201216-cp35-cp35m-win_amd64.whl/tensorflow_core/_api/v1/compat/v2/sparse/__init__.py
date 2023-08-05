# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Sparse Tensor Representation.

See also `tf.SparseTensor`.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.framework.sparse_tensor import SparseTensor
from tensorflow.python.ops.array_ops import sparse_mask as mask
from tensorflow.python.ops.math_ops import sparse_segment_mean_v2 as segment_mean
from tensorflow.python.ops.math_ops import sparse_segment_sqrt_n_v2 as segment_sqrt_n
from tensorflow.python.ops.math_ops import sparse_segment_sum_v2 as segment_sum
from tensorflow.python.ops.sparse_ops import _sparse_cross as cross
from tensorflow.python.ops.sparse_ops import _sparse_cross_hashed as cross_hashed
from tensorflow.python.ops.sparse_ops import from_dense
from tensorflow.python.ops.sparse_ops import sparse_add_v2 as add
from tensorflow.python.ops.sparse_ops import sparse_concat_v2 as concat
from tensorflow.python.ops.sparse_ops import sparse_expand_dims as expand_dims
from tensorflow.python.ops.sparse_ops import sparse_eye as eye
from tensorflow.python.ops.sparse_ops import sparse_fill_empty_rows as fill_empty_rows
from tensorflow.python.ops.sparse_ops import sparse_maximum as maximum
from tensorflow.python.ops.sparse_ops import sparse_minimum as minimum
from tensorflow.python.ops.sparse_ops import sparse_reduce_max_v2 as reduce_max
from tensorflow.python.ops.sparse_ops import sparse_reduce_sum_v2 as reduce_sum
from tensorflow.python.ops.sparse_ops import sparse_reorder as reorder
from tensorflow.python.ops.sparse_ops import sparse_reset_shape as reset_shape
from tensorflow.python.ops.sparse_ops import sparse_reshape as reshape
from tensorflow.python.ops.sparse_ops import sparse_retain as retain
from tensorflow.python.ops.sparse_ops import sparse_slice as slice
from tensorflow.python.ops.sparse_ops import sparse_softmax as softmax
from tensorflow.python.ops.sparse_ops import sparse_split_v2 as split
from tensorflow.python.ops.sparse_ops import sparse_tensor_dense_matmul as sparse_dense_matmul
from tensorflow.python.ops.sparse_ops import sparse_tensor_to_dense as to_dense
from tensorflow.python.ops.sparse_ops import sparse_to_indicator as to_indicator
from tensorflow.python.ops.sparse_ops import sparse_transpose as transpose

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v2.sparse", public_apis=None, deprecation=False,
      has_lite=False)
