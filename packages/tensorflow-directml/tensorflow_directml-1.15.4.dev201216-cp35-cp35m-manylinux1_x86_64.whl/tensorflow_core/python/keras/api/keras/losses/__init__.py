# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Built-in loss functions.

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.keras.losses import BinaryCrossentropy
from tensorflow.python.keras.losses import CategoricalCrossentropy
from tensorflow.python.keras.losses import CategoricalHinge
from tensorflow.python.keras.losses import CosineSimilarity
from tensorflow.python.keras.losses import Hinge
from tensorflow.python.keras.losses import Huber
from tensorflow.python.keras.losses import KLD
from tensorflow.python.keras.losses import KLD as kld
from tensorflow.python.keras.losses import KLD as kullback_leibler_divergence
from tensorflow.python.keras.losses import KLDivergence
from tensorflow.python.keras.losses import LogCosh
from tensorflow.python.keras.losses import Loss
from tensorflow.python.keras.losses import MAE
from tensorflow.python.keras.losses import MAE as mae
from tensorflow.python.keras.losses import MAE as mean_absolute_error
from tensorflow.python.keras.losses import MAPE
from tensorflow.python.keras.losses import MAPE as mape
from tensorflow.python.keras.losses import MAPE as mean_absolute_percentage_error
from tensorflow.python.keras.losses import MSE
from tensorflow.python.keras.losses import MSE as mean_squared_error
from tensorflow.python.keras.losses import MSE as mse
from tensorflow.python.keras.losses import MSLE
from tensorflow.python.keras.losses import MSLE as mean_squared_logarithmic_error
from tensorflow.python.keras.losses import MSLE as msle
from tensorflow.python.keras.losses import MeanAbsoluteError
from tensorflow.python.keras.losses import MeanAbsolutePercentageError
from tensorflow.python.keras.losses import MeanSquaredError
from tensorflow.python.keras.losses import MeanSquaredLogarithmicError
from tensorflow.python.keras.losses import Poisson
from tensorflow.python.keras.losses import SparseCategoricalCrossentropy
from tensorflow.python.keras.losses import SquaredHinge
from tensorflow.python.keras.losses import binary_crossentropy
from tensorflow.python.keras.losses import categorical_crossentropy
from tensorflow.python.keras.losses import categorical_hinge
from tensorflow.python.keras.losses import cosine_proximity
from tensorflow.python.keras.losses import cosine_proximity as cosine
from tensorflow.python.keras.losses import cosine_proximity as cosine_similarity
from tensorflow.python.keras.losses import deserialize
from tensorflow.python.keras.losses import get
from tensorflow.python.keras.losses import hinge
from tensorflow.python.keras.losses import logcosh
from tensorflow.python.keras.losses import poisson
from tensorflow.python.keras.losses import serialize
from tensorflow.python.keras.losses import sparse_categorical_crossentropy
from tensorflow.python.keras.losses import squared_hinge

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "keras.losses", public_apis=None, deprecation=True,
      has_lite=False)
