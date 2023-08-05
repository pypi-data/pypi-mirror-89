# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plugin/tensorboard_plugin_profile/protobuf/kernel_stats.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='plugin/tensorboard_plugin_profile/protobuf/kernel_stats.proto',
  package='tensorflow.profiler',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n=plugin/tensorboard_plugin_profile/protobuf/kernel_stats.proto\x12\x13tensorflow.profiler\"\xeb\x02\n\x0cKernelReport\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1c\n\x14registers_per_thread\x18\x02 \x01(\r\x12\x1a\n\x12static_shmem_bytes\x18\x03 \x01(\r\x12\x1b\n\x13\x64ynamic_shmem_bytes\x18\x04 \x01(\r\x12\x11\n\tblock_dim\x18\x05 \x03(\r\x12\x10\n\x08grid_dim\x18\x06 \x03(\r\x12\x19\n\x11total_duration_ns\x18\x07 \x01(\x04\x12\x17\n\x0fmin_duration_ns\x18\x08 \x01(\x04\x12\x17\n\x0fmax_duration_ns\x18\t \x01(\x04\x12#\n\x1bis_kernel_using_tensor_core\x18\n \x01(\x08\x12\"\n\x1ais_op_tensor_core_eligible\x18\x0b \x01(\x08\x12\x0f\n\x07op_name\x18\x0c \x01(\t\x12\x13\n\x0boccurrences\x18\r \x01(\r\x12\x15\n\roccupancy_pct\x18\x0e \x01(\x02\"C\n\rKernelStatsDb\x12\x32\n\x07reports\x18\x01 \x03(\x0b\x32!.tensorflow.profiler.KernelReportb\x06proto3')
)




_KERNELREPORT = _descriptor.Descriptor(
  name='KernelReport',
  full_name='tensorflow.profiler.KernelReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.profiler.KernelReport.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='registers_per_thread', full_name='tensorflow.profiler.KernelReport.registers_per_thread', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='static_shmem_bytes', full_name='tensorflow.profiler.KernelReport.static_shmem_bytes', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dynamic_shmem_bytes', full_name='tensorflow.profiler.KernelReport.dynamic_shmem_bytes', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='block_dim', full_name='tensorflow.profiler.KernelReport.block_dim', index=4,
      number=5, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='grid_dim', full_name='tensorflow.profiler.KernelReport.grid_dim', index=5,
      number=6, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_duration_ns', full_name='tensorflow.profiler.KernelReport.total_duration_ns', index=6,
      number=7, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_duration_ns', full_name='tensorflow.profiler.KernelReport.min_duration_ns', index=7,
      number=8, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_duration_ns', full_name='tensorflow.profiler.KernelReport.max_duration_ns', index=8,
      number=9, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_kernel_using_tensor_core', full_name='tensorflow.profiler.KernelReport.is_kernel_using_tensor_core', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_op_tensor_core_eligible', full_name='tensorflow.profiler.KernelReport.is_op_tensor_core_eligible', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='op_name', full_name='tensorflow.profiler.KernelReport.op_name', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='occurrences', full_name='tensorflow.profiler.KernelReport.occurrences', index=12,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='occupancy_pct', full_name='tensorflow.profiler.KernelReport.occupancy_pct', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=87,
  serialized_end=450,
)


_KERNELSTATSDB = _descriptor.Descriptor(
  name='KernelStatsDb',
  full_name='tensorflow.profiler.KernelStatsDb',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reports', full_name='tensorflow.profiler.KernelStatsDb.reports', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=452,
  serialized_end=519,
)

_KERNELSTATSDB.fields_by_name['reports'].message_type = _KERNELREPORT
DESCRIPTOR.message_types_by_name['KernelReport'] = _KERNELREPORT
DESCRIPTOR.message_types_by_name['KernelStatsDb'] = _KERNELSTATSDB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KernelReport = _reflection.GeneratedProtocolMessageType('KernelReport', (_message.Message,), {
  'DESCRIPTOR' : _KERNELREPORT,
  '__module__' : 'plugin.tensorboard_plugin_profile.protobuf.kernel_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.KernelReport)
  })
_sym_db.RegisterMessage(KernelReport)

KernelStatsDb = _reflection.GeneratedProtocolMessageType('KernelStatsDb', (_message.Message,), {
  'DESCRIPTOR' : _KERNELSTATSDB,
  '__module__' : 'plugin.tensorboard_plugin_profile.protobuf.kernel_stats_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.KernelStatsDb)
  })
_sym_db.RegisterMessage(KernelStatsDb)


# @@protoc_insertion_point(module_scope)
