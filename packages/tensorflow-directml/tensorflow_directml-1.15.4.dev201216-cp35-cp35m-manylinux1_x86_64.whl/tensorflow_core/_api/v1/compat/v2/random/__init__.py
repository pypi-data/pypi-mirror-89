# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Public API for tf.random namespace.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.compat.v2.random import experimental
from tensorflow.python.framework.random_seed import set_seed
from tensorflow.python.ops.candidate_sampling_ops import all_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import fixed_unigram_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import learned_unigram_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import log_uniform_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import uniform_candidate_sampler
from tensorflow.python.ops.random_ops import categorical
from tensorflow.python.ops.random_ops import random_gamma as gamma
from tensorflow.python.ops.random_ops import random_normal as normal
from tensorflow.python.ops.random_ops import random_poisson_v2 as poisson
from tensorflow.python.ops.random_ops import random_shuffle as shuffle
from tensorflow.python.ops.random_ops import random_uniform as uniform
from tensorflow.python.ops.random_ops import truncated_normal
from tensorflow.python.ops.stateless_random_ops import stateless_categorical
from tensorflow.python.ops.stateless_random_ops import stateless_random_normal as stateless_normal
from tensorflow.python.ops.stateless_random_ops import stateless_random_uniform as stateless_uniform
from tensorflow.python.ops.stateless_random_ops import stateless_truncated_normal

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v2.random", public_apis=None, deprecation=False,
      has_lite=False)
