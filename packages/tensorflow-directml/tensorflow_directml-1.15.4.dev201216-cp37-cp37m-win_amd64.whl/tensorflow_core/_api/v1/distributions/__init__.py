# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Core module for TensorFlow distribution objects and helpers.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.ops.distributions.bernoulli import Bernoulli
from tensorflow.python.ops.distributions.beta import Beta
from tensorflow.python.ops.distributions.categorical import Categorical
from tensorflow.python.ops.distributions.dirichlet import Dirichlet
from tensorflow.python.ops.distributions.dirichlet_multinomial import DirichletMultinomial
from tensorflow.python.ops.distributions.distribution import Distribution
from tensorflow.python.ops.distributions.distribution import FULLY_REPARAMETERIZED
from tensorflow.python.ops.distributions.distribution import NOT_REPARAMETERIZED
from tensorflow.python.ops.distributions.distribution import ReparameterizationType
from tensorflow.python.ops.distributions.exponential import Exponential
from tensorflow.python.ops.distributions.gamma import Gamma
from tensorflow.python.ops.distributions.kullback_leibler import RegisterKL
from tensorflow.python.ops.distributions.kullback_leibler import kl_divergence
from tensorflow.python.ops.distributions.laplace import Laplace
from tensorflow.python.ops.distributions.multinomial import Multinomial
from tensorflow.python.ops.distributions.normal import Normal
from tensorflow.python.ops.distributions.student_t import StudentT
from tensorflow.python.ops.distributions.uniform import Uniform

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "distributions", public_apis=None, deprecation=True,
      has_lite=False)
