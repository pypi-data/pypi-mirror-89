# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/saved_object_graph.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.protobuf import trackable_object_graph_pb2 as tensorflow_dot_core_dot_protobuf_dot_trackable__object__graph__pb2
from tensorflow.core.protobuf import struct_pb2 as tensorflow_dot_core_dot_protobuf_dot_struct__pb2
from tensorflow.core.framework import tensor_shape_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2
from tensorflow.core.framework import types_pb2 as tensorflow_dot_core_dot_framework_dot_types__pb2
from tensorflow.core.framework import versions_pb2 as tensorflow_dot_core_dot_framework_dot_versions__pb2
from tensorflow.core.framework import variable_pb2 as tensorflow_dot_core_dot_framework_dot_variable__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/saved_object_graph.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=_b('\370\001\001'),
  serialized_pb=_b('\n1tensorflow/core/protobuf/saved_object_graph.proto\x12\ntensorflow\x1a\x35tensorflow/core/protobuf/trackable_object_graph.proto\x1a%tensorflow/core/protobuf/struct.proto\x1a,tensorflow/core/framework/tensor_shape.proto\x1a%tensorflow/core/framework/types.proto\x1a(tensorflow/core/framework/versions.proto\x1a(tensorflow/core/framework/variable.proto\"\xe8\x01\n\x10SavedObjectGraph\x12&\n\x05nodes\x18\x01 \x03(\x0b\x32\x17.tensorflow.SavedObject\x12O\n\x12\x63oncrete_functions\x18\x02 \x03(\x0b\x32\x33.tensorflow.SavedObjectGraph.ConcreteFunctionsEntry\x1a[\n\x16\x43oncreteFunctionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.tensorflow.SavedConcreteFunction:\x02\x38\x01\"\xbd\x04\n\x0bSavedObject\x12R\n\x08\x63hildren\x18\x01 \x03(\x0b\x32@.tensorflow.TrackableObjectGraph.TrackableObject.ObjectReference\x12^\n\x0eslot_variables\x18\x03 \x03(\x0b\x32\x46.tensorflow.TrackableObjectGraph.TrackableObject.SlotVariableReference\x12\x32\n\x0buser_object\x18\x04 \x01(\x0b\x32\x1b.tensorflow.SavedUserObjectH\x00\x12\'\n\x05\x61sset\x18\x05 \x01(\x0b\x32\x16.tensorflow.SavedAssetH\x00\x12-\n\x08\x66unction\x18\x06 \x01(\x0b\x32\x19.tensorflow.SavedFunctionH\x00\x12-\n\x08variable\x18\x07 \x01(\x0b\x32\x19.tensorflow.SavedVariableH\x00\x12G\n\x16\x62\x61re_concrete_function\x18\x08 \x01(\x0b\x32%.tensorflow.SavedBareConcreteFunctionH\x00\x12-\n\x08\x63onstant\x18\t \x01(\x0b\x32\x19.tensorflow.SavedConstantH\x00\x12-\n\x08resource\x18\n \x01(\x0b\x32\x19.tensorflow.SavedResourceH\x00\x42\x06\n\x04kindJ\x04\x08\x02\x10\x03R\nattributes\"`\n\x0fSavedUserObject\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\'\n\x07version\x18\x02 \x01(\x0b\x32\x16.tensorflow.VersionDef\x12\x10\n\x08metadata\x18\x03 \x01(\t\"*\n\nSavedAsset\x12\x1c\n\x14\x61sset_file_def_index\x18\x01 \x01(\x05\"\\\n\rSavedFunction\x12\x1a\n\x12\x63oncrete_functions\x18\x01 \x03(\t\x12/\n\rfunction_spec\x18\x02 \x01(\x0b\x32\x18.tensorflow.FunctionSpec\"\xa8\x01\n\x15SavedConcreteFunction\x12\x14\n\x0c\x62ound_inputs\x18\x02 \x03(\x05\x12\x42\n\x1d\x63\x61nonicalized_input_signature\x18\x03 \x01(\x0b\x32\x1b.tensorflow.StructuredValue\x12\x35\n\x10output_signature\x18\x04 \x01(\x0b\x32\x1b.tensorflow.StructuredValue\"|\n\x19SavedBareConcreteFunction\x12\x1e\n\x16\x63oncrete_function_name\x18\x01 \x01(\t\x12\x19\n\x11\x61rgument_keywords\x18\x02 \x03(\t\x12$\n\x1c\x61llowed_positional_arguments\x18\x03 \x01(\x03\"\"\n\rSavedConstant\x12\x11\n\toperation\x18\x01 \x01(\t\"\xf6\x01\n\rSavedVariable\x12#\n\x05\x64type\x18\x01 \x01(\x0e\x32\x14.tensorflow.DataType\x12+\n\x05shape\x18\x02 \x01(\x0b\x32\x1c.tensorflow.TensorShapeProto\x12\x11\n\ttrainable\x18\x03 \x01(\x08\x12<\n\x0fsynchronization\x18\x04 \x01(\x0e\x32#.tensorflow.VariableSynchronization\x12\x34\n\x0b\x61ggregation\x18\x05 \x01(\x0e\x32\x1f.tensorflow.VariableAggregation\x12\x0c\n\x04name\x18\x06 \x01(\t\"\x95\x01\n\x0c\x46unctionSpec\x12\x30\n\x0b\x66ullargspec\x18\x01 \x01(\x0b\x32\x1b.tensorflow.StructuredValue\x12\x11\n\tis_method\x18\x02 \x01(\x08\x12\x34\n\x0finput_signature\x18\x05 \x01(\x0b\x32\x1b.tensorflow.StructuredValueJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05\"\x1f\n\rSavedResource\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\tB\x03\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorflow_dot_core_dot_protobuf_dot_trackable__object__graph__pb2.DESCRIPTOR,tensorflow_dot_core_dot_protobuf_dot_struct__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_types__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_versions__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_variable__pb2.DESCRIPTOR,])




_SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY = _descriptor.Descriptor(
  name='ConcreteFunctionsEntry',
  full_name='tensorflow.SavedObjectGraph.ConcreteFunctionsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorflow.SavedObjectGraph.ConcreteFunctionsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorflow.SavedObjectGraph.ConcreteFunctionsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=470,
  serialized_end=561,
)

_SAVEDOBJECTGRAPH = _descriptor.Descriptor(
  name='SavedObjectGraph',
  full_name='tensorflow.SavedObjectGraph',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nodes', full_name='tensorflow.SavedObjectGraph.nodes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='concrete_functions', full_name='tensorflow.SavedObjectGraph.concrete_functions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=329,
  serialized_end=561,
)


_SAVEDOBJECT = _descriptor.Descriptor(
  name='SavedObject',
  full_name='tensorflow.SavedObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='children', full_name='tensorflow.SavedObject.children', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slot_variables', full_name='tensorflow.SavedObject.slot_variables', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_object', full_name='tensorflow.SavedObject.user_object', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='asset', full_name='tensorflow.SavedObject.asset', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function', full_name='tensorflow.SavedObject.function', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='variable', full_name='tensorflow.SavedObject.variable', index=5,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bare_concrete_function', full_name='tensorflow.SavedObject.bare_concrete_function', index=6,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='constant', full_name='tensorflow.SavedObject.constant', index=7,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resource', full_name='tensorflow.SavedObject.resource', index=8,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='kind', full_name='tensorflow.SavedObject.kind',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=564,
  serialized_end=1137,
)


_SAVEDUSEROBJECT = _descriptor.Descriptor(
  name='SavedUserObject',
  full_name='tensorflow.SavedUserObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='tensorflow.SavedUserObject.identifier', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorflow.SavedUserObject.version', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='tensorflow.SavedUserObject.metadata', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1139,
  serialized_end=1235,
)


_SAVEDASSET = _descriptor.Descriptor(
  name='SavedAsset',
  full_name='tensorflow.SavedAsset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='asset_file_def_index', full_name='tensorflow.SavedAsset.asset_file_def_index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1237,
  serialized_end=1279,
)


_SAVEDFUNCTION = _descriptor.Descriptor(
  name='SavedFunction',
  full_name='tensorflow.SavedFunction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='concrete_functions', full_name='tensorflow.SavedFunction.concrete_functions', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function_spec', full_name='tensorflow.SavedFunction.function_spec', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1281,
  serialized_end=1373,
)


_SAVEDCONCRETEFUNCTION = _descriptor.Descriptor(
  name='SavedConcreteFunction',
  full_name='tensorflow.SavedConcreteFunction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bound_inputs', full_name='tensorflow.SavedConcreteFunction.bound_inputs', index=0,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='canonicalized_input_signature', full_name='tensorflow.SavedConcreteFunction.canonicalized_input_signature', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_signature', full_name='tensorflow.SavedConcreteFunction.output_signature', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1376,
  serialized_end=1544,
)


_SAVEDBARECONCRETEFUNCTION = _descriptor.Descriptor(
  name='SavedBareConcreteFunction',
  full_name='tensorflow.SavedBareConcreteFunction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='concrete_function_name', full_name='tensorflow.SavedBareConcreteFunction.concrete_function_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='argument_keywords', full_name='tensorflow.SavedBareConcreteFunction.argument_keywords', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allowed_positional_arguments', full_name='tensorflow.SavedBareConcreteFunction.allowed_positional_arguments', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1546,
  serialized_end=1670,
)


_SAVEDCONSTANT = _descriptor.Descriptor(
  name='SavedConstant',
  full_name='tensorflow.SavedConstant',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='operation', full_name='tensorflow.SavedConstant.operation', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1672,
  serialized_end=1706,
)


_SAVEDVARIABLE = _descriptor.Descriptor(
  name='SavedVariable',
  full_name='tensorflow.SavedVariable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.SavedVariable.dtype', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.SavedVariable.shape', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trainable', full_name='tensorflow.SavedVariable.trainable', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='synchronization', full_name='tensorflow.SavedVariable.synchronization', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='aggregation', full_name='tensorflow.SavedVariable.aggregation', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.SavedVariable.name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1709,
  serialized_end=1955,
)


_FUNCTIONSPEC = _descriptor.Descriptor(
  name='FunctionSpec',
  full_name='tensorflow.FunctionSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fullargspec', full_name='tensorflow.FunctionSpec.fullargspec', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_method', full_name='tensorflow.FunctionSpec.is_method', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_signature', full_name='tensorflow.FunctionSpec.input_signature', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1958,
  serialized_end=2107,
)


_SAVEDRESOURCE = _descriptor.Descriptor(
  name='SavedResource',
  full_name='tensorflow.SavedResource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='tensorflow.SavedResource.device', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2109,
  serialized_end=2140,
)

_SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY.fields_by_name['value'].message_type = _SAVEDCONCRETEFUNCTION
_SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY.containing_type = _SAVEDOBJECTGRAPH
_SAVEDOBJECTGRAPH.fields_by_name['nodes'].message_type = _SAVEDOBJECT
_SAVEDOBJECTGRAPH.fields_by_name['concrete_functions'].message_type = _SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY
_SAVEDOBJECT.fields_by_name['children'].message_type = tensorflow_dot_core_dot_protobuf_dot_trackable__object__graph__pb2._TRACKABLEOBJECTGRAPH_TRACKABLEOBJECT_OBJECTREFERENCE
_SAVEDOBJECT.fields_by_name['slot_variables'].message_type = tensorflow_dot_core_dot_protobuf_dot_trackable__object__graph__pb2._TRACKABLEOBJECTGRAPH_TRACKABLEOBJECT_SLOTVARIABLEREFERENCE
_SAVEDOBJECT.fields_by_name['user_object'].message_type = _SAVEDUSEROBJECT
_SAVEDOBJECT.fields_by_name['asset'].message_type = _SAVEDASSET
_SAVEDOBJECT.fields_by_name['function'].message_type = _SAVEDFUNCTION
_SAVEDOBJECT.fields_by_name['variable'].message_type = _SAVEDVARIABLE
_SAVEDOBJECT.fields_by_name['bare_concrete_function'].message_type = _SAVEDBARECONCRETEFUNCTION
_SAVEDOBJECT.fields_by_name['constant'].message_type = _SAVEDCONSTANT
_SAVEDOBJECT.fields_by_name['resource'].message_type = _SAVEDRESOURCE
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['user_object'])
_SAVEDOBJECT.fields_by_name['user_object'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['asset'])
_SAVEDOBJECT.fields_by_name['asset'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['function'])
_SAVEDOBJECT.fields_by_name['function'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['variable'])
_SAVEDOBJECT.fields_by_name['variable'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['bare_concrete_function'])
_SAVEDOBJECT.fields_by_name['bare_concrete_function'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['constant'])
_SAVEDOBJECT.fields_by_name['constant'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDOBJECT.oneofs_by_name['kind'].fields.append(
  _SAVEDOBJECT.fields_by_name['resource'])
_SAVEDOBJECT.fields_by_name['resource'].containing_oneof = _SAVEDOBJECT.oneofs_by_name['kind']
_SAVEDUSEROBJECT.fields_by_name['version'].message_type = tensorflow_dot_core_dot_framework_dot_versions__pb2._VERSIONDEF
_SAVEDFUNCTION.fields_by_name['function_spec'].message_type = _FUNCTIONSPEC
_SAVEDCONCRETEFUNCTION.fields_by_name['canonicalized_input_signature'].message_type = tensorflow_dot_core_dot_protobuf_dot_struct__pb2._STRUCTUREDVALUE
_SAVEDCONCRETEFUNCTION.fields_by_name['output_signature'].message_type = tensorflow_dot_core_dot_protobuf_dot_struct__pb2._STRUCTUREDVALUE
_SAVEDVARIABLE.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_SAVEDVARIABLE.fields_by_name['shape'].message_type = tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_SAVEDVARIABLE.fields_by_name['synchronization'].enum_type = tensorflow_dot_core_dot_framework_dot_variable__pb2._VARIABLESYNCHRONIZATION
_SAVEDVARIABLE.fields_by_name['aggregation'].enum_type = tensorflow_dot_core_dot_framework_dot_variable__pb2._VARIABLEAGGREGATION
_FUNCTIONSPEC.fields_by_name['fullargspec'].message_type = tensorflow_dot_core_dot_protobuf_dot_struct__pb2._STRUCTUREDVALUE
_FUNCTIONSPEC.fields_by_name['input_signature'].message_type = tensorflow_dot_core_dot_protobuf_dot_struct__pb2._STRUCTUREDVALUE
DESCRIPTOR.message_types_by_name['SavedObjectGraph'] = _SAVEDOBJECTGRAPH
DESCRIPTOR.message_types_by_name['SavedObject'] = _SAVEDOBJECT
DESCRIPTOR.message_types_by_name['SavedUserObject'] = _SAVEDUSEROBJECT
DESCRIPTOR.message_types_by_name['SavedAsset'] = _SAVEDASSET
DESCRIPTOR.message_types_by_name['SavedFunction'] = _SAVEDFUNCTION
DESCRIPTOR.message_types_by_name['SavedConcreteFunction'] = _SAVEDCONCRETEFUNCTION
DESCRIPTOR.message_types_by_name['SavedBareConcreteFunction'] = _SAVEDBARECONCRETEFUNCTION
DESCRIPTOR.message_types_by_name['SavedConstant'] = _SAVEDCONSTANT
DESCRIPTOR.message_types_by_name['SavedVariable'] = _SAVEDVARIABLE
DESCRIPTOR.message_types_by_name['FunctionSpec'] = _FUNCTIONSPEC
DESCRIPTOR.message_types_by_name['SavedResource'] = _SAVEDRESOURCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SavedObjectGraph = _reflection.GeneratedProtocolMessageType('SavedObjectGraph', (_message.Message,), {

  'ConcreteFunctionsEntry' : _reflection.GeneratedProtocolMessageType('ConcreteFunctionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY,
    '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.SavedObjectGraph.ConcreteFunctionsEntry)
    })
  ,
  'DESCRIPTOR' : _SAVEDOBJECTGRAPH,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedObjectGraph)
  })
_sym_db.RegisterMessage(SavedObjectGraph)
_sym_db.RegisterMessage(SavedObjectGraph.ConcreteFunctionsEntry)

SavedObject = _reflection.GeneratedProtocolMessageType('SavedObject', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDOBJECT,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedObject)
  })
_sym_db.RegisterMessage(SavedObject)

SavedUserObject = _reflection.GeneratedProtocolMessageType('SavedUserObject', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDUSEROBJECT,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedUserObject)
  })
_sym_db.RegisterMessage(SavedUserObject)

SavedAsset = _reflection.GeneratedProtocolMessageType('SavedAsset', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDASSET,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedAsset)
  })
_sym_db.RegisterMessage(SavedAsset)

SavedFunction = _reflection.GeneratedProtocolMessageType('SavedFunction', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDFUNCTION,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedFunction)
  })
_sym_db.RegisterMessage(SavedFunction)

SavedConcreteFunction = _reflection.GeneratedProtocolMessageType('SavedConcreteFunction', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDCONCRETEFUNCTION,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedConcreteFunction)
  })
_sym_db.RegisterMessage(SavedConcreteFunction)

SavedBareConcreteFunction = _reflection.GeneratedProtocolMessageType('SavedBareConcreteFunction', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDBARECONCRETEFUNCTION,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedBareConcreteFunction)
  })
_sym_db.RegisterMessage(SavedBareConcreteFunction)

SavedConstant = _reflection.GeneratedProtocolMessageType('SavedConstant', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDCONSTANT,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedConstant)
  })
_sym_db.RegisterMessage(SavedConstant)

SavedVariable = _reflection.GeneratedProtocolMessageType('SavedVariable', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDVARIABLE,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedVariable)
  })
_sym_db.RegisterMessage(SavedVariable)

FunctionSpec = _reflection.GeneratedProtocolMessageType('FunctionSpec', (_message.Message,), {
  'DESCRIPTOR' : _FUNCTIONSPEC,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.FunctionSpec)
  })
_sym_db.RegisterMessage(FunctionSpec)

SavedResource = _reflection.GeneratedProtocolMessageType('SavedResource', (_message.Message,), {
  'DESCRIPTOR' : _SAVEDRESOURCE,
  '__module__' : 'tensorflow.core.protobuf.saved_object_graph_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.SavedResource)
  })
_sym_db.RegisterMessage(SavedResource)


DESCRIPTOR._options = None
_SAVEDOBJECTGRAPH_CONCRETEFUNCTIONSENTRY._options = None
# @@protoc_insertion_point(module_scope)
