# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Import router for file_io.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow.python.lib.io.file_io import copy as Copy
from tensorflow.python.lib.io.file_io import create_dir as MkDir
from tensorflow.python.lib.io.file_io import delete_file as Remove
from tensorflow.python.lib.io.file_io import delete_recursively as DeleteRecursively
from tensorflow.python.lib.io.file_io import file_exists as Exists
from tensorflow.python.lib.io.file_io import get_matching_files as Glob
from tensorflow.python.lib.io.file_io import is_directory as IsDirectory
from tensorflow.python.lib.io.file_io import list_directory as ListDirectory
from tensorflow.python.lib.io.file_io import recursive_create_dir as MakeDirs
from tensorflow.python.lib.io.file_io import rename as Rename
from tensorflow.python.lib.io.file_io import stat as Stat
from tensorflow.python.lib.io.file_io import walk as Walk
from tensorflow.python.platform.gfile import FastGFile
from tensorflow.python.platform.gfile import GFile
from tensorflow.python.platform.gfile import GFile as Open

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.gfile", public_apis=None, deprecation=False,
      has_lite=False)
