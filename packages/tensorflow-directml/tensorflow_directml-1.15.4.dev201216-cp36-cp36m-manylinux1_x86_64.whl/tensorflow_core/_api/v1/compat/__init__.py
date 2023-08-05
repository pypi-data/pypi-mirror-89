# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Functions for Python 2 vs. 3 compatibility.

## Conversion routines
In addition to the functions below, `as_str` converts an object to a `str`.


## Types
The compatibility module also provides the following types:

* `bytes_or_text_types`
* `complex_types`
* `integral_types`
* `real_types`

"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.compat import v1
from tensorflow._api.v1.compat import v2
from tensorflow.python.compat.compat import forward_compatibility_horizon
from tensorflow.python.compat.compat import forward_compatible
from tensorflow.python.framework.tensor_shape import dimension_at_index
from tensorflow.python.framework.tensor_shape import dimension_value
from tensorflow.python.util.compat import as_bytes
from tensorflow.python.util.compat import as_str
from tensorflow.python.util.compat import as_str as as_text
from tensorflow.python.util.compat import as_str_any
from tensorflow.python.util.compat import bytes_or_text_types
from tensorflow.python.util.compat import complex_types
from tensorflow.python.util.compat import integral_types
from tensorflow.python.util.compat import path_to_str
from tensorflow.python.util.compat import real_types

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat", public_apis=None, deprecation=True,
      has_lite=False)
