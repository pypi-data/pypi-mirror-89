# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.feature_column namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.feature_column.feature_column_v2 import bucketized_column
from tensorflow.python.feature_column.feature_column_v2 import categorical_column_with_hash_bucket
from tensorflow.python.feature_column.feature_column_v2 import categorical_column_with_identity
from tensorflow.python.feature_column.feature_column_v2 import categorical_column_with_vocabulary_file_v2 as categorical_column_with_vocabulary_file
from tensorflow.python.feature_column.feature_column_v2 import categorical_column_with_vocabulary_list
from tensorflow.python.feature_column.feature_column_v2 import crossed_column
from tensorflow.python.feature_column.feature_column_v2 import embedding_column
from tensorflow.python.feature_column.feature_column_v2 import indicator_column
from tensorflow.python.feature_column.feature_column_v2 import make_parse_example_spec_v2 as make_parse_example_spec
from tensorflow.python.feature_column.feature_column_v2 import numeric_column
from tensorflow.python.feature_column.feature_column_v2 import shared_embedding_columns_v2 as shared_embeddings
from tensorflow.python.feature_column.feature_column_v2 import weighted_categorical_column
from tensorflow.python.feature_column.sequence_feature_column import sequence_categorical_column_with_hash_bucket
from tensorflow.python.feature_column.sequence_feature_column import sequence_categorical_column_with_identity
from tensorflow.python.feature_column.sequence_feature_column import sequence_categorical_column_with_vocabulary_file
from tensorflow.python.feature_column.sequence_feature_column import sequence_categorical_column_with_vocabulary_list
from tensorflow.python.feature_column.sequence_feature_column import sequence_numeric_column

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v2.feature_column", public_apis=None, deprecation=False,
      has_lite=False)
