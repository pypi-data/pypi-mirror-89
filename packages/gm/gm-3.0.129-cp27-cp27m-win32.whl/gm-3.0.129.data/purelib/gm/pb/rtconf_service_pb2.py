# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/rtconf_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import common_pb2 as gm_dot_pb_dot_common__pb2
from gm.pb import rtconf_pb2 as gm_dot_pb_dot_rtconf__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/rtconf_service.proto',
  package='rtconf.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x1agm/pb/rtconf_service.proto\x12\nrtconf.api\x1a\x12gm/pb/common.proto\x1a\x12gm/pb/rtconf.proto\x1a\x1bgoogle/protobuf/empty.proto\"F\n\x10GetParametersReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x10\n\x08owner_id\x18\x02 \x01(\t\"2\n\x10\x44\x65lParametersReq\x12\x10\n\x08owner_id\x18\x01 \x01(\t\x12\x0c\n\x04keys\x18\x02 \x03(\t\"C\n\rGetSymbolsReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x10\n\x08owner_id\x18\x02 \x01(\t2\xab\x03\n\x14RuntimeConfigService\x12\x41\n\rAddParameters\x12\x16.rtconf.api.Parameters\x1a\x16.google.protobuf.Empty\"\x00\x12\x41\n\rSetParameters\x12\x16.rtconf.api.Parameters\x1a\x16.google.protobuf.Empty\"\x00\x12G\n\rGetParameters\x12\x1c.rtconf.api.GetParametersReq\x1a\x16.rtconf.api.Parameters\"\x00\x12G\n\rDelParameters\x12\x1c.rtconf.api.DelParametersReq\x1a\x16.google.protobuf.Empty\"\x00\x12;\n\nSetSymbols\x12\x13.rtconf.api.Symbols\x1a\x16.google.protobuf.Empty\"\x00\x12>\n\nGetSymbols\x12\x19.rtconf.api.GetSymbolsReq\x1a\x13.rtconf.api.Symbols\"\x00\x62\x06proto3'
  ,
  dependencies=[gm_dot_pb_dot_common__pb2.DESCRIPTOR,gm_dot_pb_dot_rtconf__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_GETPARAMETERSREQ = _descriptor.Descriptor(
  name='GetParametersReq',
  full_name='rtconf.api.GetParametersReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='rtconf.api.GetParametersReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='rtconf.api.GetParametersReq.owner_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=111,
  serialized_end=181,
)


_DELPARAMETERSREQ = _descriptor.Descriptor(
  name='DelParametersReq',
  full_name='rtconf.api.DelParametersReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='rtconf.api.DelParametersReq.owner_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keys', full_name='rtconf.api.DelParametersReq.keys', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=183,
  serialized_end=233,
)


_GETSYMBOLSREQ = _descriptor.Descriptor(
  name='GetSymbolsReq',
  full_name='rtconf.api.GetSymbolsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='rtconf.api.GetSymbolsReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='rtconf.api.GetSymbolsReq.owner_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=235,
  serialized_end=302,
)

_GETPARAMETERSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSYMBOLSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
DESCRIPTOR.message_types_by_name['GetParametersReq'] = _GETPARAMETERSREQ
DESCRIPTOR.message_types_by_name['DelParametersReq'] = _DELPARAMETERSREQ
DESCRIPTOR.message_types_by_name['GetSymbolsReq'] = _GETSYMBOLSREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetParametersReq = _reflection.GeneratedProtocolMessageType('GetParametersReq', (_message.Message,), {
  'DESCRIPTOR' : _GETPARAMETERSREQ,
  '__module__' : 'gm.pb.rtconf_service_pb2'
  # @@protoc_insertion_point(class_scope:rtconf.api.GetParametersReq)
  })
_sym_db.RegisterMessage(GetParametersReq)

DelParametersReq = _reflection.GeneratedProtocolMessageType('DelParametersReq', (_message.Message,), {
  'DESCRIPTOR' : _DELPARAMETERSREQ,
  '__module__' : 'gm.pb.rtconf_service_pb2'
  # @@protoc_insertion_point(class_scope:rtconf.api.DelParametersReq)
  })
_sym_db.RegisterMessage(DelParametersReq)

GetSymbolsReq = _reflection.GeneratedProtocolMessageType('GetSymbolsReq', (_message.Message,), {
  'DESCRIPTOR' : _GETSYMBOLSREQ,
  '__module__' : 'gm.pb.rtconf_service_pb2'
  # @@protoc_insertion_point(class_scope:rtconf.api.GetSymbolsReq)
  })
_sym_db.RegisterMessage(GetSymbolsReq)



_RUNTIMECONFIGSERVICE = _descriptor.ServiceDescriptor(
  name='RuntimeConfigService',
  full_name='rtconf.api.RuntimeConfigService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=305,
  serialized_end=732,
  methods=[
  _descriptor.MethodDescriptor(
    name='AddParameters',
    full_name='rtconf.api.RuntimeConfigService.AddParameters',
    index=0,
    containing_service=None,
    input_type=gm_dot_pb_dot_rtconf__pb2._PARAMETERS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetParameters',
    full_name='rtconf.api.RuntimeConfigService.SetParameters',
    index=1,
    containing_service=None,
    input_type=gm_dot_pb_dot_rtconf__pb2._PARAMETERS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetParameters',
    full_name='rtconf.api.RuntimeConfigService.GetParameters',
    index=2,
    containing_service=None,
    input_type=_GETPARAMETERSREQ,
    output_type=gm_dot_pb_dot_rtconf__pb2._PARAMETERS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DelParameters',
    full_name='rtconf.api.RuntimeConfigService.DelParameters',
    index=3,
    containing_service=None,
    input_type=_DELPARAMETERSREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetSymbols',
    full_name='rtconf.api.RuntimeConfigService.SetSymbols',
    index=4,
    containing_service=None,
    input_type=gm_dot_pb_dot_rtconf__pb2._SYMBOLS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetSymbols',
    full_name='rtconf.api.RuntimeConfigService.GetSymbols',
    index=5,
    containing_service=None,
    input_type=_GETSYMBOLSREQ,
    output_type=gm_dot_pb_dot_rtconf__pb2._SYMBOLS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_RUNTIMECONFIGSERVICE)

DESCRIPTOR.services_by_name['RuntimeConfigService'] = _RUNTIMECONFIGSERVICE

# @@protoc_insertion_point(module_scope)
