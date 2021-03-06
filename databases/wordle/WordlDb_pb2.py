# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WordlDb.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='WordlDb.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rWordlDb.proto\"V\n\nGameRecord\x12\x0c\n\x04game\x18\x01 \x01(\t\x12\x10\n\x08\x61ttempts\x18\x02 \x01(\x05\x12\x14\n\x0cmax_attempts\x18\x03 \x01(\x05\x12\x12\n\nextra_data\x18\x04 \x01(\t\"\x1c\n\x0cGameModifier\x12\x0c\n\x04game\x18\x01 \x01(\t\"*\n\x0cUserModifier\x12\x1a\n\x12suggested_starters\x18\x01 \x03(\t\"\xa8\x03\n\nUserRecord\x12\x17\n\x0flast_known_name\x18\x03 \x01(\t\x12$\n\ruser_modifier\x18\x05 \x01(\x0b\x32\r.UserModifier\x12\x34\n\rclassic_games\x18\x01 \x03(\x0b\x32\x1d.UserRecord.ClassicGamesEntry\x12\x32\n\x0c\x63ustom_games\x18\x02 \x03(\x0b\x32\x1c.UserRecord.CustomGamesEntry\x12-\n\tmodifiers\x18\x04 \x03(\x0b\x32\x1a.UserRecord.ModifiersEntry\x1a@\n\x11\x43lassicGamesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.GameRecord:\x02\x38\x01\x1a?\n\x10\x43ustomGamesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.GameRecord:\x02\x38\x01\x1a?\n\x0eModifiersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1c\n\x05value\x18\x02 \x01(\x0b\x32\r.GameModifier:\x02\x38\x01\"<\n\x13\x44\x61ilySeasonModifier\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x11\n\tword_pool\x18\x02 \x03(\t\"\xc0\x01\n\x0cWordleSeason\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08\x66ilename\x18\x02 \x01(\t\x12\'\n\x05users\x18\x03 \x03(\x0b\x32\x18.WordleSeason.UsersEntry\x12,\n\x0e\x64\x61ily_modifier\x18\x04 \x03(\x0b\x32\x14.DailySeasonModifier\x1a\x39\n\nUsersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.UserRecord:\x02\x38\x01\"\xd3\x02\n\x11WordlSeasonFileDb\x12\x14\n\x0c\x63urrent_file\x18\x01 \x01(\t\x12\x1b\n\x13\x63urrent_season_name\x18\x02 \x01(\t\x12M\n\x17\x66ilename_to_season_name\x18\x03 \x03(\x0b\x32,.WordlSeasonFileDb.FilenameToSeasonNameEntry\x12\x45\n\x12reprint_registered\x18\x04 \x03(\x0b\x32).WordlSeasonFileDb.ReprintRegisteredEntry\x1a;\n\x19\x46ilenameToSeasonNameEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x38\n\x16ReprintRegisteredEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x08:\x02\x38\x01'
)




_GAMERECORD = _descriptor.Descriptor(
  name='GameRecord',
  full_name='GameRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='game', full_name='GameRecord.game', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attempts', full_name='GameRecord.attempts', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_attempts', full_name='GameRecord.max_attempts', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extra_data', full_name='GameRecord.extra_data', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=103,
)


_GAMEMODIFIER = _descriptor.Descriptor(
  name='GameModifier',
  full_name='GameModifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='game', full_name='GameModifier.game', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=105,
  serialized_end=133,
)


_USERMODIFIER = _descriptor.Descriptor(
  name='UserModifier',
  full_name='UserModifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='suggested_starters', full_name='UserModifier.suggested_starters', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=177,
)


_USERRECORD_CLASSICGAMESENTRY = _descriptor.Descriptor(
  name='ClassicGamesEntry',
  full_name='UserRecord.ClassicGamesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='UserRecord.ClassicGamesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='UserRecord.ClassicGamesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=410,
  serialized_end=474,
)

_USERRECORD_CUSTOMGAMESENTRY = _descriptor.Descriptor(
  name='CustomGamesEntry',
  full_name='UserRecord.CustomGamesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='UserRecord.CustomGamesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='UserRecord.CustomGamesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=476,
  serialized_end=539,
)

_USERRECORD_MODIFIERSENTRY = _descriptor.Descriptor(
  name='ModifiersEntry',
  full_name='UserRecord.ModifiersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='UserRecord.ModifiersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='UserRecord.ModifiersEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=541,
  serialized_end=604,
)

_USERRECORD = _descriptor.Descriptor(
  name='UserRecord',
  full_name='UserRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='last_known_name', full_name='UserRecord.last_known_name', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_modifier', full_name='UserRecord.user_modifier', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='classic_games', full_name='UserRecord.classic_games', index=2,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='custom_games', full_name='UserRecord.custom_games', index=3,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='modifiers', full_name='UserRecord.modifiers', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_USERRECORD_CLASSICGAMESENTRY, _USERRECORD_CUSTOMGAMESENTRY, _USERRECORD_MODIFIERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=604,
)


_DAILYSEASONMODIFIER = _descriptor.Descriptor(
  name='DailySeasonModifier',
  full_name='DailySeasonModifier',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='identifier', full_name='DailySeasonModifier.identifier', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='word_pool', full_name='DailySeasonModifier.word_pool', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=606,
  serialized_end=666,
)


_WORDLESEASON_USERSENTRY = _descriptor.Descriptor(
  name='UsersEntry',
  full_name='WordleSeason.UsersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='WordleSeason.UsersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='WordleSeason.UsersEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=804,
  serialized_end=861,
)

_WORDLESEASON = _descriptor.Descriptor(
  name='WordleSeason',
  full_name='WordleSeason',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='WordleSeason.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='WordleSeason.filename', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='users', full_name='WordleSeason.users', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='daily_modifier', full_name='WordleSeason.daily_modifier', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_WORDLESEASON_USERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=669,
  serialized_end=861,
)


_WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY = _descriptor.Descriptor(
  name='FilenameToSeasonNameEntry',
  full_name='WordlSeasonFileDb.FilenameToSeasonNameEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='WordlSeasonFileDb.FilenameToSeasonNameEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='WordlSeasonFileDb.FilenameToSeasonNameEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1086,
  serialized_end=1145,
)

_WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY = _descriptor.Descriptor(
  name='ReprintRegisteredEntry',
  full_name='WordlSeasonFileDb.ReprintRegisteredEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='WordlSeasonFileDb.ReprintRegisteredEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='WordlSeasonFileDb.ReprintRegisteredEntry.value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1147,
  serialized_end=1203,
)

_WORDLSEASONFILEDB = _descriptor.Descriptor(
  name='WordlSeasonFileDb',
  full_name='WordlSeasonFileDb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_file', full_name='WordlSeasonFileDb.current_file', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='current_season_name', full_name='WordlSeasonFileDb.current_season_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename_to_season_name', full_name='WordlSeasonFileDb.filename_to_season_name', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reprint_registered', full_name='WordlSeasonFileDb.reprint_registered', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY, _WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=864,
  serialized_end=1203,
)

_USERRECORD_CLASSICGAMESENTRY.fields_by_name['value'].message_type = _GAMERECORD
_USERRECORD_CLASSICGAMESENTRY.containing_type = _USERRECORD
_USERRECORD_CUSTOMGAMESENTRY.fields_by_name['value'].message_type = _GAMERECORD
_USERRECORD_CUSTOMGAMESENTRY.containing_type = _USERRECORD
_USERRECORD_MODIFIERSENTRY.fields_by_name['value'].message_type = _GAMEMODIFIER
_USERRECORD_MODIFIERSENTRY.containing_type = _USERRECORD
_USERRECORD.fields_by_name['user_modifier'].message_type = _USERMODIFIER
_USERRECORD.fields_by_name['classic_games'].message_type = _USERRECORD_CLASSICGAMESENTRY
_USERRECORD.fields_by_name['custom_games'].message_type = _USERRECORD_CUSTOMGAMESENTRY
_USERRECORD.fields_by_name['modifiers'].message_type = _USERRECORD_MODIFIERSENTRY
_WORDLESEASON_USERSENTRY.fields_by_name['value'].message_type = _USERRECORD
_WORDLESEASON_USERSENTRY.containing_type = _WORDLESEASON
_WORDLESEASON.fields_by_name['users'].message_type = _WORDLESEASON_USERSENTRY
_WORDLESEASON.fields_by_name['daily_modifier'].message_type = _DAILYSEASONMODIFIER
_WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY.containing_type = _WORDLSEASONFILEDB
_WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY.containing_type = _WORDLSEASONFILEDB
_WORDLSEASONFILEDB.fields_by_name['filename_to_season_name'].message_type = _WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY
_WORDLSEASONFILEDB.fields_by_name['reprint_registered'].message_type = _WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY
DESCRIPTOR.message_types_by_name['GameRecord'] = _GAMERECORD
DESCRIPTOR.message_types_by_name['GameModifier'] = _GAMEMODIFIER
DESCRIPTOR.message_types_by_name['UserModifier'] = _USERMODIFIER
DESCRIPTOR.message_types_by_name['UserRecord'] = _USERRECORD
DESCRIPTOR.message_types_by_name['DailySeasonModifier'] = _DAILYSEASONMODIFIER
DESCRIPTOR.message_types_by_name['WordleSeason'] = _WORDLESEASON
DESCRIPTOR.message_types_by_name['WordlSeasonFileDb'] = _WORDLSEASONFILEDB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GameRecord = _reflection.GeneratedProtocolMessageType('GameRecord', (_message.Message,), {
  'DESCRIPTOR' : _GAMERECORD,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:GameRecord)
  })
_sym_db.RegisterMessage(GameRecord)

GameModifier = _reflection.GeneratedProtocolMessageType('GameModifier', (_message.Message,), {
  'DESCRIPTOR' : _GAMEMODIFIER,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:GameModifier)
  })
_sym_db.RegisterMessage(GameModifier)

UserModifier = _reflection.GeneratedProtocolMessageType('UserModifier', (_message.Message,), {
  'DESCRIPTOR' : _USERMODIFIER,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:UserModifier)
  })
_sym_db.RegisterMessage(UserModifier)

UserRecord = _reflection.GeneratedProtocolMessageType('UserRecord', (_message.Message,), {

  'ClassicGamesEntry' : _reflection.GeneratedProtocolMessageType('ClassicGamesEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERRECORD_CLASSICGAMESENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:UserRecord.ClassicGamesEntry)
    })
  ,

  'CustomGamesEntry' : _reflection.GeneratedProtocolMessageType('CustomGamesEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERRECORD_CUSTOMGAMESENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:UserRecord.CustomGamesEntry)
    })
  ,

  'ModifiersEntry' : _reflection.GeneratedProtocolMessageType('ModifiersEntry', (_message.Message,), {
    'DESCRIPTOR' : _USERRECORD_MODIFIERSENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:UserRecord.ModifiersEntry)
    })
  ,
  'DESCRIPTOR' : _USERRECORD,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:UserRecord)
  })
_sym_db.RegisterMessage(UserRecord)
_sym_db.RegisterMessage(UserRecord.ClassicGamesEntry)
_sym_db.RegisterMessage(UserRecord.CustomGamesEntry)
_sym_db.RegisterMessage(UserRecord.ModifiersEntry)

DailySeasonModifier = _reflection.GeneratedProtocolMessageType('DailySeasonModifier', (_message.Message,), {
  'DESCRIPTOR' : _DAILYSEASONMODIFIER,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:DailySeasonModifier)
  })
_sym_db.RegisterMessage(DailySeasonModifier)

WordleSeason = _reflection.GeneratedProtocolMessageType('WordleSeason', (_message.Message,), {

  'UsersEntry' : _reflection.GeneratedProtocolMessageType('UsersEntry', (_message.Message,), {
    'DESCRIPTOR' : _WORDLESEASON_USERSENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:WordleSeason.UsersEntry)
    })
  ,
  'DESCRIPTOR' : _WORDLESEASON,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:WordleSeason)
  })
_sym_db.RegisterMessage(WordleSeason)
_sym_db.RegisterMessage(WordleSeason.UsersEntry)

WordlSeasonFileDb = _reflection.GeneratedProtocolMessageType('WordlSeasonFileDb', (_message.Message,), {

  'FilenameToSeasonNameEntry' : _reflection.GeneratedProtocolMessageType('FilenameToSeasonNameEntry', (_message.Message,), {
    'DESCRIPTOR' : _WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:WordlSeasonFileDb.FilenameToSeasonNameEntry)
    })
  ,

  'ReprintRegisteredEntry' : _reflection.GeneratedProtocolMessageType('ReprintRegisteredEntry', (_message.Message,), {
    'DESCRIPTOR' : _WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY,
    '__module__' : 'WordlDb_pb2'
    # @@protoc_insertion_point(class_scope:WordlSeasonFileDb.ReprintRegisteredEntry)
    })
  ,
  'DESCRIPTOR' : _WORDLSEASONFILEDB,
  '__module__' : 'WordlDb_pb2'
  # @@protoc_insertion_point(class_scope:WordlSeasonFileDb)
  })
_sym_db.RegisterMessage(WordlSeasonFileDb)
_sym_db.RegisterMessage(WordlSeasonFileDb.FilenameToSeasonNameEntry)
_sym_db.RegisterMessage(WordlSeasonFileDb.ReprintRegisteredEntry)


_USERRECORD_CLASSICGAMESENTRY._options = None
_USERRECORD_CUSTOMGAMESENTRY._options = None
_USERRECORD_MODIFIERSENTRY._options = None
_WORDLESEASON_USERSENTRY._options = None
_WORDLSEASONFILEDB_FILENAMETOSEASONNAMEENTRY._options = None
_WORDLSEASONFILEDB_REPRINTREGISTEREDENTRY._options = None
# @@protoc_insertion_point(module_scope)
