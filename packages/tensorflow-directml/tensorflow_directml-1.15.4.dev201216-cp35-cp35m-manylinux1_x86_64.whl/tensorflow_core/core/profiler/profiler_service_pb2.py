# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/profiler/profiler_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.framework import graph_pb2 as tensorflow_dot_core_dot_framework_dot_graph__pb2
from tensorflow.core.profiler import op_profile_pb2 as tensorflow_dot_core_dot_profiler_dot_op__profile__pb2
from tensorflow.core.protobuf import config_pb2 as tensorflow_dot_core_dot_protobuf_dot_config__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/profiler/profiler_service.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n/tensorflow/core/profiler/profiler_service.proto\x12\ntensorflow\x1a%tensorflow/core/framework/graph.proto\x1a)tensorflow/core/profiler/op_profile.proto\x1a%tensorflow/core/protobuf/config.proto\"-\n\x0eProfileOptions\x12\x1b\n\x13include_dataset_ops\x18\x01 \x01(\x08\"B\n\x12ToolRequestOptions\x12\x16\n\x0eoutput_formats\x18\x02 \x01(\t\x12\x14\n\x0csave_to_repo\x18\x03 \x01(\x08\"\xc9\x02\n\x0eProfileRequest\x12\x13\n\x0b\x64uration_ms\x18\x01 \x01(\x04\x12\x12\n\nmax_events\x18\x02 \x01(\x04\x12\r\n\x05tools\x18\x03 \x03(\t\x12\x41\n\x0ctool_options\x18\x08 \x03(\x0b\x32+.tensorflow.ProfileRequest.ToolOptionsEntry\x12(\n\x04opts\x18\x04 \x01(\x0b\x32\x1a.tensorflow.ProfileOptions\x12\x17\n\x0frepository_root\x18\x05 \x01(\t\x12\x12\n\nsession_id\x18\x06 \x01(\t\x12\x11\n\thost_name\x18\x07 \x01(\t\x1aR\n\x10ToolOptionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.tensorflow.ToolRequestOptions:\x02\x38\x01\"-\n\x0fProfileToolData\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x90\x02\n\x0fProfileResponse\x12/\n\x11\x63omputation_graph\x18\x02 \x03(\x0b\x32\x14.tensorflow.GraphDef\x12-\n\x0chlo_metadata\x18\x05 \x01(\x0b\x32\x17.tensorflow.RunMetadata\x12\x15\n\rencoded_trace\x18\x03 \x01(\x0c\x12;\n\nop_profile\x18\x04 \x01(\x0b\x32\'.tensorflow.profiler.op_profile.Profile\x12.\n\ttool_data\x18\x06 \x03(\x0b\x32\x1b.tensorflow.ProfileToolData\x12\x13\n\x0b\x65mpty_trace\x18\x07 \x01(\x08J\x04\x08\x01\x10\x02\"R\n\x0eMonitorRequest\x12\x13\n\x0b\x64uration_ms\x18\x01 \x01(\x04\x12\x18\n\x10monitoring_level\x18\x02 \x01(\x05\x12\x11\n\ttimestamp\x18\x03 \x01(\x08\"\x1f\n\x0fMonitorResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t2\x9d\x01\n\x0fProfilerService\x12\x44\n\x07Profile\x12\x1a.tensorflow.ProfileRequest\x1a\x1b.tensorflow.ProfileResponse\"\x00\x12\x44\n\x07Monitor\x12\x1a.tensorflow.MonitorRequest\x1a\x1b.tensorflow.MonitorResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_graph__pb2.DESCRIPTOR,tensorflow_dot_core_dot_profiler_dot_op__profile__pb2.DESCRIPTOR,tensorflow_dot_core_dot_protobuf_dot_config__pb2.DESCRIPTOR,])




_PROFILEOPTIONS = _descriptor.Descriptor(
  name='ProfileOptions',
  full_name='tensorflow.ProfileOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='include_dataset_ops', full_name='tensorflow.ProfileOptions.include_dataset_ops', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=184,
  serialized_end=229,
)


_TOOLREQUESTOPTIONS = _descriptor.Descriptor(
  name='ToolRequestOptions',
  full_name='tensorflow.ToolRequestOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='output_formats', full_name='tensorflow.ToolRequestOptions.output_formats', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='save_to_repo', full_name='tensorflow.ToolRequestOptions.save_to_repo', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=231,
  serialized_end=297,
)


_PROFILEREQUEST_TOOLOPTIONSENTRY = _descriptor.Descriptor(
  name='ToolOptionsEntry',
  full_name='tensorflow.ProfileRequest.ToolOptionsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorflow.ProfileRequest.ToolOptionsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorflow.ProfileRequest.ToolOptionsEntry.value', index=1,
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
  serialized_start=547,
  serialized_end=629,
)

_PROFILEREQUEST = _descriptor.Descriptor(
  name='ProfileRequest',
  full_name='tensorflow.ProfileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='duration_ms', full_name='tensorflow.ProfileRequest.duration_ms', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_events', full_name='tensorflow.ProfileRequest.max_events', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tools', full_name='tensorflow.ProfileRequest.tools', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tool_options', full_name='tensorflow.ProfileRequest.tool_options', index=3,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opts', full_name='tensorflow.ProfileRequest.opts', index=4,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='repository_root', full_name='tensorflow.ProfileRequest.repository_root', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='tensorflow.ProfileRequest.session_id', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host_name', full_name='tensorflow.ProfileRequest.host_name', index=7,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_PROFILEREQUEST_TOOLOPTIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=300,
  serialized_end=629,
)


_PROFILETOOLDATA = _descriptor.Descriptor(
  name='ProfileToolData',
  full_name='tensorflow.ProfileToolData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.ProfileToolData.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='tensorflow.ProfileToolData.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=631,
  serialized_end=676,
)


_PROFILERESPONSE = _descriptor.Descriptor(
  name='ProfileResponse',
  full_name='tensorflow.ProfileResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='computation_graph', full_name='tensorflow.ProfileResponse.computation_graph', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hlo_metadata', full_name='tensorflow.ProfileResponse.hlo_metadata', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoded_trace', full_name='tensorflow.ProfileResponse.encoded_trace', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_profile', full_name='tensorflow.ProfileResponse.op_profile', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tool_data', full_name='tensorflow.ProfileResponse.tool_data', index=4,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='empty_trace', full_name='tensorflow.ProfileResponse.empty_trace', index=5,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=679,
  serialized_end=951,
)


_MONITORREQUEST = _descriptor.Descriptor(
  name='MonitorRequest',
  full_name='tensorflow.MonitorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='duration_ms', full_name='tensorflow.MonitorRequest.duration_ms', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='monitoring_level', full_name='tensorflow.MonitorRequest.monitoring_level', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='tensorflow.MonitorRequest.timestamp', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=953,
  serialized_end=1035,
)


_MONITORRESPONSE = _descriptor.Descriptor(
  name='MonitorResponse',
  full_name='tensorflow.MonitorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='tensorflow.MonitorResponse.data', index=0,
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
  serialized_start=1037,
  serialized_end=1068,
)

_PROFILEREQUEST_TOOLOPTIONSENTRY.fields_by_name['value'].message_type = _TOOLREQUESTOPTIONS
_PROFILEREQUEST_TOOLOPTIONSENTRY.containing_type = _PROFILEREQUEST
_PROFILEREQUEST.fields_by_name['tool_options'].message_type = _PROFILEREQUEST_TOOLOPTIONSENTRY
_PROFILEREQUEST.fields_by_name['opts'].message_type = _PROFILEOPTIONS
_PROFILERESPONSE.fields_by_name['computation_graph'].message_type = tensorflow_dot_core_dot_framework_dot_graph__pb2._GRAPHDEF
_PROFILERESPONSE.fields_by_name['hlo_metadata'].message_type = tensorflow_dot_core_dot_protobuf_dot_config__pb2._RUNMETADATA
_PROFILERESPONSE.fields_by_name['op_profile'].message_type = tensorflow_dot_core_dot_profiler_dot_op__profile__pb2._PROFILE
_PROFILERESPONSE.fields_by_name['tool_data'].message_type = _PROFILETOOLDATA
DESCRIPTOR.message_types_by_name['ProfileOptions'] = _PROFILEOPTIONS
DESCRIPTOR.message_types_by_name['ToolRequestOptions'] = _TOOLREQUESTOPTIONS
DESCRIPTOR.message_types_by_name['ProfileRequest'] = _PROFILEREQUEST
DESCRIPTOR.message_types_by_name['ProfileToolData'] = _PROFILETOOLDATA
DESCRIPTOR.message_types_by_name['ProfileResponse'] = _PROFILERESPONSE
DESCRIPTOR.message_types_by_name['MonitorRequest'] = _MONITORREQUEST
DESCRIPTOR.message_types_by_name['MonitorResponse'] = _MONITORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProfileOptions = _reflection.GeneratedProtocolMessageType('ProfileOptions', (_message.Message,), {
  'DESCRIPTOR' : _PROFILEOPTIONS,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ProfileOptions)
  })
_sym_db.RegisterMessage(ProfileOptions)

ToolRequestOptions = _reflection.GeneratedProtocolMessageType('ToolRequestOptions', (_message.Message,), {
  'DESCRIPTOR' : _TOOLREQUESTOPTIONS,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ToolRequestOptions)
  })
_sym_db.RegisterMessage(ToolRequestOptions)

ProfileRequest = _reflection.GeneratedProtocolMessageType('ProfileRequest', (_message.Message,), {

  'ToolOptionsEntry' : _reflection.GeneratedProtocolMessageType('ToolOptionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _PROFILEREQUEST_TOOLOPTIONSENTRY,
    '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.ProfileRequest.ToolOptionsEntry)
    })
  ,
  'DESCRIPTOR' : _PROFILEREQUEST,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ProfileRequest)
  })
_sym_db.RegisterMessage(ProfileRequest)
_sym_db.RegisterMessage(ProfileRequest.ToolOptionsEntry)

ProfileToolData = _reflection.GeneratedProtocolMessageType('ProfileToolData', (_message.Message,), {
  'DESCRIPTOR' : _PROFILETOOLDATA,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ProfileToolData)
  })
_sym_db.RegisterMessage(ProfileToolData)

ProfileResponse = _reflection.GeneratedProtocolMessageType('ProfileResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROFILERESPONSE,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ProfileResponse)
  })
_sym_db.RegisterMessage(ProfileResponse)

MonitorRequest = _reflection.GeneratedProtocolMessageType('MonitorRequest', (_message.Message,), {
  'DESCRIPTOR' : _MONITORREQUEST,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.MonitorRequest)
  })
_sym_db.RegisterMessage(MonitorRequest)

MonitorResponse = _reflection.GeneratedProtocolMessageType('MonitorResponse', (_message.Message,), {
  'DESCRIPTOR' : _MONITORRESPONSE,
  '__module__' : 'tensorflow.core.profiler.profiler_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.MonitorResponse)
  })
_sym_db.RegisterMessage(MonitorResponse)


_PROFILEREQUEST_TOOLOPTIONSENTRY._options = None

_PROFILERSERVICE = _descriptor.ServiceDescriptor(
  name='ProfilerService',
  full_name='tensorflow.ProfilerService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1071,
  serialized_end=1228,
  methods=[
  _descriptor.MethodDescriptor(
    name='Profile',
    full_name='tensorflow.ProfilerService.Profile',
    index=0,
    containing_service=None,
    input_type=_PROFILEREQUEST,
    output_type=_PROFILERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Monitor',
    full_name='tensorflow.ProfilerService.Monitor',
    index=1,
    containing_service=None,
    input_type=_MONITORREQUEST,
    output_type=_MONITORRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROFILERSERVICE)

DESCRIPTOR.services_by_name['ProfilerService'] = _PROFILERSERVICE

# @@protoc_insertion_point(module_scope)
