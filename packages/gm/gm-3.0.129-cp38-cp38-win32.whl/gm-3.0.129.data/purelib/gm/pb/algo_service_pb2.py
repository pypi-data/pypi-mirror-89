# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/algo_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import common_pb2 as gm_dot_pb_dot_common__pb2
from gm.pb import account_pb2 as gm_dot_pb_dot_account__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/algo_service.proto',
  package='trade.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x18gm/pb/algo_service.proto\x12\ttrade.api\x1a\x12gm/pb/common.proto\x1a\x13gm/pb/account.proto\x1a\x1bgoogle/protobuf/empty.proto\"\xf7\x01\n\x10GetAlgoOrdersReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x12\n\naccount_id\x18\x02 \x01(\t\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x06 \x01(\t\x12\x0f\n\x07symbols\x18\x03 \x03(\t\x12\x12\n\ncl_ord_ids\x18\x04 \x03(\t\x12?\n\nproperties\x18\x05 \x03(\x0b\x32+.trade.api.GetAlgoOrdersReq.PropertiesEntry\x1a\x31\n\x0fPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\x9b\x02\n\x0b\x41lgoService\x12?\n\x0fPlaceAlgoOrders\x12\x14.core.api.AlgoOrders\x1a\x14.core.api.AlgoOrders\"\x00\x12\x42\n\x10\x43\x61ncelAlgoOrders\x12\x14.core.api.AlgoOrders\x1a\x16.google.protobuf.Empty\"\x00\x12\x41\n\x0fPauseAlgoOrders\x12\x14.core.api.AlgoOrders\x1a\x16.google.protobuf.Empty\"\x00\x12\x44\n\rGetAlgoOrders\x12\x1b.trade.api.GetAlgoOrdersReq\x1a\x14.core.api.AlgoOrders\"\x00\x62\x06proto3'
  ,
  dependencies=[gm_dot_pb_dot_common__pb2.DESCRIPTOR,gm_dot_pb_dot_account__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_GETALGOORDERSREQ_PROPERTIESENTRY = _descriptor.Descriptor(
  name='PropertiesEntry',
  full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='trade.api.GetAlgoOrdersReq.PropertiesEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=308,
  serialized_end=357,
)

_GETALGOORDERSREQ = _descriptor.Descriptor(
  name='GetAlgoOrdersReq',
  full_name='trade.api.GetAlgoOrdersReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='trade.api.GetAlgoOrdersReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_id', full_name='trade.api.GetAlgoOrdersReq.account_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_name', full_name='trade.api.GetAlgoOrdersReq.account_name', index=2,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='symbols', full_name='trade.api.GetAlgoOrdersReq.symbols', index=3,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cl_ord_ids', full_name='trade.api.GetAlgoOrdersReq.cl_ord_ids', index=4,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='properties', full_name='trade.api.GetAlgoOrdersReq.properties', index=5,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETALGOORDERSREQ_PROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=110,
  serialized_end=357,
)

_GETALGOORDERSREQ_PROPERTIESENTRY.containing_type = _GETALGOORDERSREQ
_GETALGOORDERSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETALGOORDERSREQ.fields_by_name['properties'].message_type = _GETALGOORDERSREQ_PROPERTIESENTRY
DESCRIPTOR.message_types_by_name['GetAlgoOrdersReq'] = _GETALGOORDERSREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAlgoOrdersReq = _reflection.GeneratedProtocolMessageType('GetAlgoOrdersReq', (_message.Message,), {

  'PropertiesEntry' : _reflection.GeneratedProtocolMessageType('PropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _GETALGOORDERSREQ_PROPERTIESENTRY,
    '__module__' : 'gm.pb.algo_service_pb2'
    # @@protoc_insertion_point(class_scope:trade.api.GetAlgoOrdersReq.PropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _GETALGOORDERSREQ,
  '__module__' : 'gm.pb.algo_service_pb2'
  # @@protoc_insertion_point(class_scope:trade.api.GetAlgoOrdersReq)
  })
_sym_db.RegisterMessage(GetAlgoOrdersReq)
_sym_db.RegisterMessage(GetAlgoOrdersReq.PropertiesEntry)


_GETALGOORDERSREQ_PROPERTIESENTRY._options = None

_ALGOSERVICE = _descriptor.ServiceDescriptor(
  name='AlgoService',
  full_name='trade.api.AlgoService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=360,
  serialized_end=643,
  methods=[
  _descriptor.MethodDescriptor(
    name='PlaceAlgoOrders',
    full_name='trade.api.AlgoService.PlaceAlgoOrders',
    index=0,
    containing_service=None,
    input_type=gm_dot_pb_dot_account__pb2._ALGOORDERS,
    output_type=gm_dot_pb_dot_account__pb2._ALGOORDERS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='CancelAlgoOrders',
    full_name='trade.api.AlgoService.CancelAlgoOrders',
    index=1,
    containing_service=None,
    input_type=gm_dot_pb_dot_account__pb2._ALGOORDERS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='PauseAlgoOrders',
    full_name='trade.api.AlgoService.PauseAlgoOrders',
    index=2,
    containing_service=None,
    input_type=gm_dot_pb_dot_account__pb2._ALGOORDERS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetAlgoOrders',
    full_name='trade.api.AlgoService.GetAlgoOrders',
    index=3,
    containing_service=None,
    input_type=_GETALGOORDERSREQ,
    output_type=gm_dot_pb_dot_account__pb2._ALGOORDERS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ALGOSERVICE)

DESCRIPTOR.services_by_name['AlgoService'] = _ALGOSERVICE

# @@protoc_insertion_point(module_scope)
