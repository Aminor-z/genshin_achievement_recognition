# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Guiar.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Guiar.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bGuiar.proto\"F\n\tGuiarItem\x12\n\n\x02id\x18\x02 \x01(\x05\x12\r\n\x05state\x18\x03 \x01(\x08\x12\x0e\n\x06\x64\x61ta_a\x18\x04 \x01(\x05\x12\x0e\n\x06\x64\x61ta_b\x18\x05 \x01(\x05\"F\n\nGuiarBlock\x12\x0b\n\x03uid\x18\x01 \x01(\x05\x12\x10\n\x08group_id\x18\x02 \x01(\x05\x12\x19\n\x05items\x18\x03 \x03(\x0b\x32\n.GuiarItemb\x06proto3'
)




_GUIARITEM = _descriptor.Descriptor(
  name='GuiarItem',
  full_name='GuiarItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='GuiarItem.id', index=0,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='GuiarItem.state', index=1,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_a', full_name='GuiarItem.data_a', index=2,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_b', full_name='GuiarItem.data_b', index=3,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=15,
  serialized_end=85,
)


_GUIARBLOCK = _descriptor.Descriptor(
  name='GuiarBlock',
  full_name='GuiarBlock',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='uid', full_name='GuiarBlock.uid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_id', full_name='GuiarBlock.group_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='items', full_name='GuiarBlock.items', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=87,
  serialized_end=157,
)

_GUIARBLOCK.fields_by_name['items'].message_type = _GUIARITEM
DESCRIPTOR.message_types_by_name['GuiarItem'] = _GUIARITEM
DESCRIPTOR.message_types_by_name['GuiarBlock'] = _GUIARBLOCK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GuiarItem = _reflection.GeneratedProtocolMessageType('GuiarItem', (_message.Message,), {
  'DESCRIPTOR' : _GUIARITEM,
  '__module__' : 'Guiar_pb2'
  # @@protoc_insertion_point(class_scope:GuiarItem)
  })
_sym_db.RegisterMessage(GuiarItem)

GuiarBlock = _reflection.GeneratedProtocolMessageType('GuiarBlock', (_message.Message,), {
  'DESCRIPTOR' : _GUIARBLOCK,
  '__module__' : 'Guiar_pb2'
  # @@protoc_insertion_point(class_scope:GuiarBlock)
  })
_sym_db.RegisterMessage(GuiarBlock)


# @@protoc_insertion_point(module_scope)
