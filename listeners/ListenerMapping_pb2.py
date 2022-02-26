# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ListenerMapping.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15ListenerMapping.proto\"\'\n\x12\x41vailableListeners\x12\x11\n\tlisteners\x18\x01 \x03(\t\"\xbc\x01\n\x0fListenerMapping\x12S\n\x1b\x63hannel_to_listener_mapping\x18\x01 \x03(\x0b\x32..ListenerMapping.ChannelToListenerMappingEntry\x1aT\n\x1d\x43hannelToListenerMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.AvailableListeners:\x02\x38\x01')



_AVAILABLELISTENERS = DESCRIPTOR.message_types_by_name['AvailableListeners']
_LISTENERMAPPING = DESCRIPTOR.message_types_by_name['ListenerMapping']
_LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY = _LISTENERMAPPING.nested_types_by_name['ChannelToListenerMappingEntry']
AvailableListeners = _reflection.GeneratedProtocolMessageType('AvailableListeners', (_message.Message,), {
  'DESCRIPTOR' : _AVAILABLELISTENERS,
  '__module__' : 'ListenerMapping_pb2'
  # @@protoc_insertion_point(class_scope:AvailableListeners)
  })
_sym_db.RegisterMessage(AvailableListeners)

ListenerMapping = _reflection.GeneratedProtocolMessageType('ListenerMapping', (_message.Message,), {

  'ChannelToListenerMappingEntry' : _reflection.GeneratedProtocolMessageType('ChannelToListenerMappingEntry', (_message.Message,), {
    'DESCRIPTOR' : _LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY,
    '__module__' : 'ListenerMapping_pb2'
    # @@protoc_insertion_point(class_scope:ListenerMapping.ChannelToListenerMappingEntry)
    })
  ,
  'DESCRIPTOR' : _LISTENERMAPPING,
  '__module__' : 'ListenerMapping_pb2'
  # @@protoc_insertion_point(class_scope:ListenerMapping)
  })
_sym_db.RegisterMessage(ListenerMapping)
_sym_db.RegisterMessage(ListenerMapping.ChannelToListenerMappingEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY._options = None
  _LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY._serialized_options = b'8\001'
  _AVAILABLELISTENERS._serialized_start=25
  _AVAILABLELISTENERS._serialized_end=64
  _LISTENERMAPPING._serialized_start=67
  _LISTENERMAPPING._serialized_end=255
  _LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY._serialized_start=171
  _LISTENERMAPPING_CHANNELTOLISTENERMAPPINGENTRY._serialized_end=255
# @@protoc_insertion_point(module_scope)
