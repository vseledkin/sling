# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: third_party/syntaxnet/dragnn/protos/spec.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='third_party/syntaxnet/dragnn/protos/spec.proto',
  package='syntaxnet.dragnn',
  syntax='proto2',
  serialized_pb=_b('\n.third_party/syntaxnet/dragnn/protos/spec.proto\x12\x10syntaxnet.dragnn\"X\n\nMasterSpec\x12\x32\n\tcomponent\x18\x01 \x03(\x0b\x32\x1f.syntaxnet.dragnn.ComponentSpecJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06\"\xa6\x04\n\rComponentSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x41\n\x11transition_system\x18\x02 \x01(\x0b\x32&.syntaxnet.dragnn.RegisteredModuleSpec\x12,\n\x08resource\x18\x03 \x03(\x0b\x32\x1a.syntaxnet.dragnn.Resource\x12<\n\rfixed_feature\x18\x04 \x03(\x0b\x32%.syntaxnet.dragnn.FixedFeatureChannel\x12>\n\x0elinked_feature\x18\x05 \x03(\x0b\x32&.syntaxnet.dragnn.LinkedFeatureChannel\x12\x43\n\x11\x66\x61st_text_feature\x18\x06 \x03(\x0b\x32(.syntaxnet.dragnn.FastTextFeatureChannel\x12<\n\x0cnetwork_unit\x18\x07 \x01(\x0b\x32&.syntaxnet.dragnn.RegisteredModuleSpec\x12\x37\n\x07\x62\x61\x63kend\x18\x08 \x01(\x0b\x32&.syntaxnet.dragnn.RegisteredModuleSpec\x12\x13\n\x0bnum_actions\x18\t \x01(\x05\x12\x41\n\x11\x63omponent_builder\x18\x0b \x01(\x0b\x32&.syntaxnet.dragnn.RegisteredModuleSpecJ\x04\x08\n\x10\x0b\"\xae\x01\n\x14RegisteredModuleSpec\x12\x17\n\x0fregistered_name\x18\x01 \x01(\t\x12J\n\nparameters\x18\x02 \x03(\x0b\x32\x36.syntaxnet.dragnn.RegisteredModuleSpec.ParametersEntry\x1a\x31\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\">\n\x08Resource\x12\x0c\n\x04name\x18\x01 \x01(\t\x12$\n\x04part\x18\x02 \x03(\x0b\x32\x16.syntaxnet.dragnn.Part\"H\n\x04Part\x12\x14\n\x0c\x66ile_pattern\x18\x01 \x01(\t\x12\x13\n\x0b\x66ile_format\x18\x02 \x01(\t\x12\x15\n\rrecord_format\x18\x03 \x01(\t\"\xf5\x01\n\x13\x46ixedFeatureChannel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x66ml\x18\x02 \x01(\t\x12\x15\n\rembedding_dim\x18\x03 \x01(\x05\x12\x17\n\x0fvocabulary_size\x18\x04 \x01(\x05\x12\x0c\n\x04size\x18\x05 \x01(\x05\x12\x13\n\x0bis_constant\x18\t \x01(\x08\x12?\n\x1bpretrained_embedding_matrix\x18\x07 \x01(\x0b\x32\x1a.syntaxnet.dragnn.Resource\x12)\n\x05vocab\x18\x08 \x01(\x0b\x32\x1a.syntaxnet.dragnn.ResourceJ\x04\x08\x06\x10\x07\"\xa1\x01\n\x14LinkedFeatureChannel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x66ml\x18\x02 \x01(\t\x12\x15\n\rembedding_dim\x18\x03 \x01(\x05\x12\x0c\n\x04size\x18\x04 \x01(\x05\x12\x18\n\x10source_component\x18\x05 \x01(\t\x12\x19\n\x11source_translator\x18\x06 \x01(\t\x12\x14\n\x0csource_layer\x18\x07 \x01(\t\"\x7f\n\x16\x46\x61stTextFeatureChannel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x66ml\x18\x02 \x01(\t\x12\x15\n\rembedding_dim\x18\x03 \x01(\x05\x12\x33\n\x0f\x66\x61st_text_model\x18\x07 \x01(\x0b\x32\x1a.syntaxnet.dragnn.Resource\"\x99\x06\n\tGridPoint\x12\x1a\n\rlearning_rate\x18\x01 \x01(\x01:\x03\x30.1\x12\x15\n\x08momentum\x18\x02 \x01(\x01:\x03\x30.9\x12\x18\n\ndecay_base\x18\x10 \x01(\x01:\x04\x30.96\x12\x19\n\x0b\x64\x65\x63\x61y_steps\x18\x03 \x01(\x05:\x04\x31\x30\x30\x30\x12\x1d\n\x0f\x64\x65\x63\x61y_staircase\x18\x11 \x01(\x08:\x04true\x12\x0f\n\x04seed\x18\x04 \x01(\x05:\x01\x30\x12!\n\x0flearning_method\x18\x07 \x01(\t:\x08momentum\x12!\n\x12use_moving_average\x18\x08 \x01(\x08:\x05\x66\x61lse\x12\x1e\n\x0e\x61verage_weight\x18\t \x01(\x01:\x06\x30.9999\x12\x17\n\x0c\x64ropout_rate\x18\n \x01(\x01:\x01\x31\x12\"\n\x16recurrent_dropout_rate\x18\x14 \x01(\x01:\x02-1\x12\x1d\n\x12gradient_clip_norm\x18\x0b \x01(\x01:\x01\x30\x12T\n\x18\x63omposite_optimizer_spec\x18\x0c \x01(\x0b\x32\x32.syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec\x12\x18\n\nadam_beta1\x18\r \x01(\x01:\x04\x30.01\x12\x1a\n\nadam_beta2\x18\x0e \x01(\x01:\x06\x30.9999\x12\x17\n\x08\x61\x64\x61m_eps\x18\x0f \x01(\x01:\x05\x31\x65-08\x12-\n\x1dl2_regularization_coefficient\x18\x12 \x01(\x01:\x06\x30.0001\x12\x1a\n\x0fself_norm_alpha\x18\x13 \x01(\x01:\x01\x30\x12#\n\x1bself_norm_components_filter\x18\x15 \x01(\t\x1a\x90\x01\n\x16\x43ompositeOptimizerSpec\x12,\n\x07method1\x18\x01 \x01(\x0b\x32\x1b.syntaxnet.dragnn.GridPoint\x12,\n\x07method2\x18\x02 \x01(\x0b\x32\x1b.syntaxnet.dragnn.GridPoint\x12\x1a\n\x12switch_after_steps\x18\x03 \x01(\x05J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07\"j\n\x0bTrainTarget\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x19\n\x11\x63omponent_weights\x18\x02 \x03(\x01\x12\x1b\n\x13unroll_using_oracle\x18\x03 \x03(\x08\x12\x15\n\tmax_index\x18\x04 \x01(\x05:\x02-1')
)




_MASTERSPEC = _descriptor.Descriptor(
  name='MasterSpec',
  full_name='syntaxnet.dragnn.MasterSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='component', full_name='syntaxnet.dragnn.MasterSpec.component', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=156,
)


_COMPONENTSPEC = _descriptor.Descriptor(
  name='ComponentSpec',
  full_name='syntaxnet.dragnn.ComponentSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.ComponentSpec.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transition_system', full_name='syntaxnet.dragnn.ComponentSpec.transition_system', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='resource', full_name='syntaxnet.dragnn.ComponentSpec.resource', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fixed_feature', full_name='syntaxnet.dragnn.ComponentSpec.fixed_feature', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='linked_feature', full_name='syntaxnet.dragnn.ComponentSpec.linked_feature', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fast_text_feature', full_name='syntaxnet.dragnn.ComponentSpec.fast_text_feature', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='network_unit', full_name='syntaxnet.dragnn.ComponentSpec.network_unit', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='backend', full_name='syntaxnet.dragnn.ComponentSpec.backend', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='num_actions', full_name='syntaxnet.dragnn.ComponentSpec.num_actions', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='component_builder', full_name='syntaxnet.dragnn.ComponentSpec.component_builder', index=9,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=709,
)


_REGISTEREDMODULESPEC_PARAMETERSENTRY = _descriptor.Descriptor(
  name='ParametersEntry',
  full_name='syntaxnet.dragnn.RegisteredModuleSpec.ParametersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='syntaxnet.dragnn.RegisteredModuleSpec.ParametersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='syntaxnet.dragnn.RegisteredModuleSpec.ParametersEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=837,
  serialized_end=886,
)

_REGISTEREDMODULESPEC = _descriptor.Descriptor(
  name='RegisteredModuleSpec',
  full_name='syntaxnet.dragnn.RegisteredModuleSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='registered_name', full_name='syntaxnet.dragnn.RegisteredModuleSpec.registered_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='syntaxnet.dragnn.RegisteredModuleSpec.parameters', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_REGISTEREDMODULESPEC_PARAMETERSENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=712,
  serialized_end=886,
)


_RESOURCE = _descriptor.Descriptor(
  name='Resource',
  full_name='syntaxnet.dragnn.Resource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.Resource.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='part', full_name='syntaxnet.dragnn.Resource.part', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=888,
  serialized_end=950,
)


_PART = _descriptor.Descriptor(
  name='Part',
  full_name='syntaxnet.dragnn.Part',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_pattern', full_name='syntaxnet.dragnn.Part.file_pattern', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file_format', full_name='syntaxnet.dragnn.Part.file_format', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='record_format', full_name='syntaxnet.dragnn.Part.record_format', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=952,
  serialized_end=1024,
)


_FIXEDFEATURECHANNEL = _descriptor.Descriptor(
  name='FixedFeatureChannel',
  full_name='syntaxnet.dragnn.FixedFeatureChannel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.FixedFeatureChannel.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fml', full_name='syntaxnet.dragnn.FixedFeatureChannel.fml', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='embedding_dim', full_name='syntaxnet.dragnn.FixedFeatureChannel.embedding_dim', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vocabulary_size', full_name='syntaxnet.dragnn.FixedFeatureChannel.vocabulary_size', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='syntaxnet.dragnn.FixedFeatureChannel.size', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_constant', full_name='syntaxnet.dragnn.FixedFeatureChannel.is_constant', index=5,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pretrained_embedding_matrix', full_name='syntaxnet.dragnn.FixedFeatureChannel.pretrained_embedding_matrix', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vocab', full_name='syntaxnet.dragnn.FixedFeatureChannel.vocab', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1027,
  serialized_end=1272,
)


_LINKEDFEATURECHANNEL = _descriptor.Descriptor(
  name='LinkedFeatureChannel',
  full_name='syntaxnet.dragnn.LinkedFeatureChannel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.LinkedFeatureChannel.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fml', full_name='syntaxnet.dragnn.LinkedFeatureChannel.fml', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='embedding_dim', full_name='syntaxnet.dragnn.LinkedFeatureChannel.embedding_dim', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='syntaxnet.dragnn.LinkedFeatureChannel.size', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='source_component', full_name='syntaxnet.dragnn.LinkedFeatureChannel.source_component', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='source_translator', full_name='syntaxnet.dragnn.LinkedFeatureChannel.source_translator', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='source_layer', full_name='syntaxnet.dragnn.LinkedFeatureChannel.source_layer', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1275,
  serialized_end=1436,
)


_FASTTEXTFEATURECHANNEL = _descriptor.Descriptor(
  name='FastTextFeatureChannel',
  full_name='syntaxnet.dragnn.FastTextFeatureChannel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.FastTextFeatureChannel.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fml', full_name='syntaxnet.dragnn.FastTextFeatureChannel.fml', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='embedding_dim', full_name='syntaxnet.dragnn.FastTextFeatureChannel.embedding_dim', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fast_text_model', full_name='syntaxnet.dragnn.FastTextFeatureChannel.fast_text_model', index=3,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1438,
  serialized_end=1565,
)


_GRIDPOINT_COMPOSITEOPTIMIZERSPEC = _descriptor.Descriptor(
  name='CompositeOptimizerSpec',
  full_name='syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='method1', full_name='syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec.method1', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method2', full_name='syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec.method2', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='switch_after_steps', full_name='syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec.switch_after_steps', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2205,
  serialized_end=2349,
)

_GRIDPOINT = _descriptor.Descriptor(
  name='GridPoint',
  full_name='syntaxnet.dragnn.GridPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='learning_rate', full_name='syntaxnet.dragnn.GridPoint.learning_rate', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='momentum', full_name='syntaxnet.dragnn.GridPoint.momentum', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.9),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decay_base', full_name='syntaxnet.dragnn.GridPoint.decay_base', index=2,
      number=16, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.96),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decay_steps', full_name='syntaxnet.dragnn.GridPoint.decay_steps', index=3,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decay_staircase', full_name='syntaxnet.dragnn.GridPoint.decay_staircase', index=4,
      number=17, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seed', full_name='syntaxnet.dragnn.GridPoint.seed', index=5,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='learning_method', full_name='syntaxnet.dragnn.GridPoint.learning_method', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("momentum").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='use_moving_average', full_name='syntaxnet.dragnn.GridPoint.use_moving_average', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='average_weight', full_name='syntaxnet.dragnn.GridPoint.average_weight', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.9999),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dropout_rate', full_name='syntaxnet.dragnn.GridPoint.dropout_rate', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='recurrent_dropout_rate', full_name='syntaxnet.dragnn.GridPoint.recurrent_dropout_rate', index=10,
      number=20, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(-1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gradient_clip_norm', full_name='syntaxnet.dragnn.GridPoint.gradient_clip_norm', index=11,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='composite_optimizer_spec', full_name='syntaxnet.dragnn.GridPoint.composite_optimizer_spec', index=12,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adam_beta1', full_name='syntaxnet.dragnn.GridPoint.adam_beta1', index=13,
      number=13, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.01),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adam_beta2', full_name='syntaxnet.dragnn.GridPoint.adam_beta2', index=14,
      number=14, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.9999),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adam_eps', full_name='syntaxnet.dragnn.GridPoint.adam_eps', index=15,
      number=15, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1e-08),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='l2_regularization_coefficient', full_name='syntaxnet.dragnn.GridPoint.l2_regularization_coefficient', index=16,
      number=18, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.0001),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='self_norm_alpha', full_name='syntaxnet.dragnn.GridPoint.self_norm_alpha', index=17,
      number=19, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='self_norm_components_filter', full_name='syntaxnet.dragnn.GridPoint.self_norm_components_filter', index=18,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_GRIDPOINT_COMPOSITEOPTIMIZERSPEC, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1568,
  serialized_end=2361,
)


_TRAINTARGET = _descriptor.Descriptor(
  name='TrainTarget',
  full_name='syntaxnet.dragnn.TrainTarget',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='syntaxnet.dragnn.TrainTarget.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='component_weights', full_name='syntaxnet.dragnn.TrainTarget.component_weights', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unroll_using_oracle', full_name='syntaxnet.dragnn.TrainTarget.unroll_using_oracle', index=2,
      number=3, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_index', full_name='syntaxnet.dragnn.TrainTarget.max_index', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2363,
  serialized_end=2469,
)

_MASTERSPEC.fields_by_name['component'].message_type = _COMPONENTSPEC
_COMPONENTSPEC.fields_by_name['transition_system'].message_type = _REGISTEREDMODULESPEC
_COMPONENTSPEC.fields_by_name['resource'].message_type = _RESOURCE
_COMPONENTSPEC.fields_by_name['fixed_feature'].message_type = _FIXEDFEATURECHANNEL
_COMPONENTSPEC.fields_by_name['linked_feature'].message_type = _LINKEDFEATURECHANNEL
_COMPONENTSPEC.fields_by_name['fast_text_feature'].message_type = _FASTTEXTFEATURECHANNEL
_COMPONENTSPEC.fields_by_name['network_unit'].message_type = _REGISTEREDMODULESPEC
_COMPONENTSPEC.fields_by_name['backend'].message_type = _REGISTEREDMODULESPEC
_COMPONENTSPEC.fields_by_name['component_builder'].message_type = _REGISTEREDMODULESPEC
_REGISTEREDMODULESPEC_PARAMETERSENTRY.containing_type = _REGISTEREDMODULESPEC
_REGISTEREDMODULESPEC.fields_by_name['parameters'].message_type = _REGISTEREDMODULESPEC_PARAMETERSENTRY
_RESOURCE.fields_by_name['part'].message_type = _PART
_FIXEDFEATURECHANNEL.fields_by_name['pretrained_embedding_matrix'].message_type = _RESOURCE
_FIXEDFEATURECHANNEL.fields_by_name['vocab'].message_type = _RESOURCE
_FASTTEXTFEATURECHANNEL.fields_by_name['fast_text_model'].message_type = _RESOURCE
_GRIDPOINT_COMPOSITEOPTIMIZERSPEC.fields_by_name['method1'].message_type = _GRIDPOINT
_GRIDPOINT_COMPOSITEOPTIMIZERSPEC.fields_by_name['method2'].message_type = _GRIDPOINT
_GRIDPOINT_COMPOSITEOPTIMIZERSPEC.containing_type = _GRIDPOINT
_GRIDPOINT.fields_by_name['composite_optimizer_spec'].message_type = _GRIDPOINT_COMPOSITEOPTIMIZERSPEC
DESCRIPTOR.message_types_by_name['MasterSpec'] = _MASTERSPEC
DESCRIPTOR.message_types_by_name['ComponentSpec'] = _COMPONENTSPEC
DESCRIPTOR.message_types_by_name['RegisteredModuleSpec'] = _REGISTEREDMODULESPEC
DESCRIPTOR.message_types_by_name['Resource'] = _RESOURCE
DESCRIPTOR.message_types_by_name['Part'] = _PART
DESCRIPTOR.message_types_by_name['FixedFeatureChannel'] = _FIXEDFEATURECHANNEL
DESCRIPTOR.message_types_by_name['LinkedFeatureChannel'] = _LINKEDFEATURECHANNEL
DESCRIPTOR.message_types_by_name['FastTextFeatureChannel'] = _FASTTEXTFEATURECHANNEL
DESCRIPTOR.message_types_by_name['GridPoint'] = _GRIDPOINT
DESCRIPTOR.message_types_by_name['TrainTarget'] = _TRAINTARGET
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MasterSpec = _reflection.GeneratedProtocolMessageType('MasterSpec', (_message.Message,), dict(
  DESCRIPTOR = _MASTERSPEC,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.MasterSpec)
  ))
_sym_db.RegisterMessage(MasterSpec)

ComponentSpec = _reflection.GeneratedProtocolMessageType('ComponentSpec', (_message.Message,), dict(
  DESCRIPTOR = _COMPONENTSPEC,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.ComponentSpec)
  ))
_sym_db.RegisterMessage(ComponentSpec)

RegisteredModuleSpec = _reflection.GeneratedProtocolMessageType('RegisteredModuleSpec', (_message.Message,), dict(

  ParametersEntry = _reflection.GeneratedProtocolMessageType('ParametersEntry', (_message.Message,), dict(
    DESCRIPTOR = _REGISTEREDMODULESPEC_PARAMETERSENTRY,
    __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
    # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.RegisteredModuleSpec.ParametersEntry)
    ))
  ,
  DESCRIPTOR = _REGISTEREDMODULESPEC,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.RegisteredModuleSpec)
  ))
_sym_db.RegisterMessage(RegisteredModuleSpec)
_sym_db.RegisterMessage(RegisteredModuleSpec.ParametersEntry)

Resource = _reflection.GeneratedProtocolMessageType('Resource', (_message.Message,), dict(
  DESCRIPTOR = _RESOURCE,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.Resource)
  ))
_sym_db.RegisterMessage(Resource)

Part = _reflection.GeneratedProtocolMessageType('Part', (_message.Message,), dict(
  DESCRIPTOR = _PART,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.Part)
  ))
_sym_db.RegisterMessage(Part)

FixedFeatureChannel = _reflection.GeneratedProtocolMessageType('FixedFeatureChannel', (_message.Message,), dict(
  DESCRIPTOR = _FIXEDFEATURECHANNEL,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.FixedFeatureChannel)
  ))
_sym_db.RegisterMessage(FixedFeatureChannel)

LinkedFeatureChannel = _reflection.GeneratedProtocolMessageType('LinkedFeatureChannel', (_message.Message,), dict(
  DESCRIPTOR = _LINKEDFEATURECHANNEL,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.LinkedFeatureChannel)
  ))
_sym_db.RegisterMessage(LinkedFeatureChannel)

FastTextFeatureChannel = _reflection.GeneratedProtocolMessageType('FastTextFeatureChannel', (_message.Message,), dict(
  DESCRIPTOR = _FASTTEXTFEATURECHANNEL,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.FastTextFeatureChannel)
  ))
_sym_db.RegisterMessage(FastTextFeatureChannel)

GridPoint = _reflection.GeneratedProtocolMessageType('GridPoint', (_message.Message,), dict(

  CompositeOptimizerSpec = _reflection.GeneratedProtocolMessageType('CompositeOptimizerSpec', (_message.Message,), dict(
    DESCRIPTOR = _GRIDPOINT_COMPOSITEOPTIMIZERSPEC,
    __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
    # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.GridPoint.CompositeOptimizerSpec)
    ))
  ,
  DESCRIPTOR = _GRIDPOINT,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.GridPoint)
  ))
_sym_db.RegisterMessage(GridPoint)
_sym_db.RegisterMessage(GridPoint.CompositeOptimizerSpec)

TrainTarget = _reflection.GeneratedProtocolMessageType('TrainTarget', (_message.Message,), dict(
  DESCRIPTOR = _TRAINTARGET,
  __module__ = 'third_party.syntaxnet.dragnn.protos.spec_pb2'
  # @@protoc_insertion_point(class_scope:syntaxnet.dragnn.TrainTarget)
  ))
_sym_db.RegisterMessage(TrainTarget)


_REGISTEREDMODULESPEC_PARAMETERSENTRY.has_options = True
_REGISTEREDMODULESPEC_PARAMETERSENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
