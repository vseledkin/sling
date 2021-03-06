# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Basic network units used in assembling DRAGNN graphs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import tensorflow as tf
from dragnn.python import check
from dragnn.python import dragnn_ops
from dragnn.python import registry
from tensorflow.python.ops import nn
from tensorflow.python.ops import tensor_array_ops as ta
from tensorflow.python.platform import tf_logging as logging


def linked_embeddings_name(channel_id):
    """Returns the name of the linked embedding matrix for some channel ID."""
    return 'linked_embedding_matrix_%d' % channel_id


def fixed_embeddings_name(channel_id):
    """Returns the name of the fixed embedding matrix for some channel ID."""
    return 'fixed_embedding_matrix_%d' % channel_id


class StoredActivations(object):
    """Wrapper around stored activation vectors.

    Because activations are produced and consumed in different layouts by bulk
    vs. dynamic components, this class provides a simple common
    interface/conversion API. It can be constructed from either a TensorArray
    (dynamic) or a Tensor (bulk), and the resulting object to use for lookups is
    either bulk_tensor (for bulk components) or dynamic_tensor (for dynamic
    components).
    """

    def __init__(self, tensor=None, array=None, stride=None, dim=None):
        """Creates ops for converting the input to either format.

        If 'tensor' is used, then a conversion from [stride * steps, dim] to
        [steps + 1, stride, dim] is performed for dynamic_tensor reads.

        If 'array' is used, then a conversion from [steps + 1, stride, dim] to
        [stride * steps, dim] is performed for bulk_tensor reads.

        Args:
          tensor: Bulk tensor input.
          array: TensorArray dynamic input.
          stride: stride of bulk tensor. Not used for dynamic.
          dim: dim of bulk tensor. Not used for dynamic.
        """
        if tensor is not None:
            check.IsNone(array, 'Cannot initialize from tensor and array')
            check.NotNone(stride, 'Stride is required for bulk tensor')
            check.NotNone(dim, 'Dim is required for bulk tensor')

            self._bulk_tensor = tensor
            with tf.name_scope('convert_to_dyn'):
                tensor = tf.reshape(tensor, [stride, -1, dim])
                tensor = tf.transpose(tensor, perm=[1, 0, 2])
                pad = tf.zeros([1, stride, dim], dtype=tensor.dtype)
                self._array_tensor = tf.concat([pad, tensor], 0)

        if array is not None:
            check.IsNone(tensor, 'Cannot initialize from both tensor and array')
            with tf.name_scope('convert_to_bulk'):
                self._bulk_tensor = convert_network_state_tensorarray(array)
            with tf.name_scope('convert_to_dyn'):
                self._array_tensor = array.stack()

    @property
    def bulk_tensor(self):
        return self._bulk_tensor

    @property
    def dynamic_tensor(self):
        return self._array_tensor


class NamedTensor(object):
    """Container for a tensor with associated name and dimension attributes."""

    def __init__(self, tensor, name, dim=None):
        """Inits NamedTensor with tensor, name and optional dim."""
        self.tensor = tensor
        self.name = name
        self.dim = dim


def add_embeddings(channel_id, feature_spec, seed=None):
    """Adds a variable for the embedding of a given fixed feature.

    Supports pre-trained or randomly initialized embeddings.

    Args:
      channel_id: Numeric id of the fixed feature channel
      feature_spec: Feature spec protobuf of type FixedFeatureChannel
      seed: used for random initializer

    Returns:
      tf.Variable object corresponding to the embedding for that feature.

    Raises:
      RuntimeError: if more the pretrained embeddings are specified in resources
          containing more than one part.
    """
    check.Gt(feature_spec.embedding_dim, 0,
             'Embeddings requested for non-embedded feature: %s' % feature_spec)
    name = fixed_embeddings_name(channel_id)
    shape = [feature_spec.vocabulary_size, feature_spec.embedding_dim]
    if feature_spec.HasField('pretrained_embedding_matrix'):
        if len(feature_spec.pretrained_embedding_matrix.part) > 1:
            raise RuntimeError('pretrained_embedding_matrix resource contains '
                               'more than one part:\n%s',
                               str(feature_spec.pretrained_embedding_matrix))
        if len(feature_spec.vocab.part) > 1:
            raise RuntimeError('vocab resource contains more than one part:\n%s',
                               str(feature_spec.vocab))
        seed1, seed2 = tf.get_seed(seed)
        embeddings = dragnn_ops.word_embedding_initializer(
            vectors=feature_spec.pretrained_embedding_matrix.part[0].file_pattern,
            vocabulary=feature_spec.vocab.part[0].file_pattern,
            seed=seed1,
            seed2=seed2)
        return tf.get_variable(name, initializer=tf.reshape(embeddings, shape))
    else:
        return tf.get_variable(
            name,
            shape,
            initializer=tf.random_normal_initializer(
                stddev=1.0 / feature_spec.embedding_dim ** .5, seed=seed))


def embedding_lookup(embedding_matrix, ids, batch_size):
    """Performs an embedding lookup followed by aggregation.

    Args:
      embedding_matrix: float Tensor from which to do the lookup.
      ids: int Tensor vectors to look up in the embedding_matrix.
      size: int number of output rows. Needed since some output rows may be empty.

    Returns:
      Summed embedding vectors according to indices.
    """
    num_cols = tf.shape(ids)[0] // batch_size

    # Keep only valid (i.e. > -1) feature ids, and get their batch indices.
    valid = tf.where(ids > -1)
    ids = tf.gather(ids, valid)
    batch_indices = tf.cast(valid, tf.int32) // num_cols

    embeddings = tf.nn.embedding_lookup([embedding_matrix], ids)
    embeddings = tf.unsorted_segment_sum(embeddings, batch_indices, batch_size)
    return embeddings


def fixed_feature_lookup(component, state, channel_id, batch_size):
    """Looks up fixed features and passes them through embeddings.

    Args:
      component: Component object in which to look up the fixed features.
      state: MasterState object for the live MasterState.
      channel_id: int id of the fixed feature to look up.
      batch_size: int Tensor of current batch size.

    Returns:
      NamedTensor object containing the embedding vectors.
    """
    feature_spec = component.spec.fixed_feature[channel_id]
    check.Gt(feature_spec.embedding_dim, 0,
             'Embeddings requested for non-embedded feature: %s' % feature_spec)
    dim = feature_spec.embedding_dim
    embedding_matrix = component.get_variable(fixed_embeddings_name(channel_id))

    with tf.name_scope(
            name='fixed_embedding_' + feature_spec.name, values=[embedding_matrix]):
        ids = dragnn_ops.extract_fixed_features(
            state.handle, batch_size, component=component.name,
            channel_id=channel_id, max_num_ids=feature_spec.size)
        embeddings = embedding_lookup(embedding_matrix, ids, batch_size)
        return NamedTensor(
            tf.reshape(embeddings, [-1, dim]), feature_spec.name, dim=dim)


def fast_text_feature_lookup(component, state, channel_id, batch_size):
    """Looks up fast text features.

    Args:
      component: Component object in which to look up the fixed features.
      state: MasterState object for the live MasterState.
      channel_id: int id of the fixed feature to look up.
      batch_size: int Tensor of current batch size.

    Returns:
      NamedTensor object containing the embedding vectors.
    """
    feature_spec = component.spec.fast_text_feature[channel_id]
    check.Gt(feature_spec.embedding_dim, 0,
             'Embeddings requested for non-embedded feature: %s' % feature_spec)
    dim = feature_spec.embedding_dim

    # with tf.name_scope(
    #    name='fast_text_embedding_' + feature_spec.name, values=[embedding_matrix]):
    embeddings = dragnn_ops.extract_fast_text_features(
        state.handle, batch_size, component=component.name,
        channel_id=channel_id)
    return NamedTensor(
        tf.reshape(embeddings, [-1, dim]), feature_spec.name, dim=dim)


def get_input_tensor(fixed_embeddings, linked_embeddings, fast_text_embeddings):
    """Helper function for constructing an input tensor from all the features.

    Args:
      fixed_embeddings: list of NamedTensor objects for fixed feature channels
      linked_embeddings: list of NamedTensor objects for linked feature channels

    Returns:
      a tensor of shape [N, D], where D is the total input dimension of the
          concatenated feature channels

    Raises:
      RuntimeError: if no features, fixed or linked, are configured.
    """
    embeddings = fixed_embeddings + linked_embeddings + fast_text_embeddings
    if not embeddings:
        raise RuntimeError('There needs to be at least one feature set defined.')

    # Concat_v2 takes care of optimizing away the concatenation
    # operation in the case when there is exactly one embedding input.
    return tf.concat([e.tensor for e in embeddings], 1, name="feature_vector")


def get_input_tensor_with_stride(fixed_embeddings, linked_embeddings, fast_text_embeddings, tride):
    """Constructs an input tensor with a separate dimension for steps.

    Args:
      fixed_embeddings: list of NamedTensor objects for fixed feature channels
      linked_embeddings: list of NamedTensor objects for linked feature channels
      stride: int stride (i.e. batch size) to use to reshape the input

    Returns:
      a tensor of shape [stride, num_steps, D], where D is the total input
          dimension of the concatenated feature channels
    """
    input_tensor = get_input_tensor(fixed_embeddings, linked_embeddings, fast_text_embeddings)
    shape = tf.shape(input_tensor)
    return tf.reshape(input_tensor, [stride, -1, shape[1]])


def convert_network_state_tensorarray(tensorarray):
    """Converts a source TensorArray to a source Tensor.

    Performs a permutation between the steps * [stride, D] shape of a
    source TensorArray and the (flattened) [stride * steps, D] shape of
    a source Tensor.

    The TensorArrays used during recurrence have an additional zeroth step that
    needs to be removed.

    Args:
      tensorarray: TensorArray object to be converted.

    Returns:
      Tensor object after conversion.
    """
    tensor = tensorarray.stack()  # Results in a [steps, stride, D] tensor.
    tensor = tf.slice(tensor, [1, 0, 0], [-1, -1, -1])  # Lop off the 0th step.
    tensor = tf.transpose(tensor, [1, 0, 2])  # Switch steps and stride.
    return tf.reshape(tensor, [-1, tf.shape(tensor)[2]])


def pass_through_embedding_matrix(act_block, embedding_matrix, step_idx):
    """Passes the activations through the embedding_matrix.

    Takes care to handle out of bounds lookups.

    Args:
      act_block: matrix of activations.
      embedding_matrix: matrix of weights.
      step_idx: vector containing step indices, with -1 indicating out of bounds.

    Returns:
      the embedded activations.
    """
    # Indicator vector for out of bounds lookups.
    step_idx_mask = tf.expand_dims(tf.equal(step_idx, -1), -1)

    # Pad the last column of the activation vectors with the indicator.
    act_block = tf.concat([act_block, tf.to_float(step_idx_mask)], 1)
    return tf.matmul(act_block, embedding_matrix)


def lookup_named_tensor(name, named_tensors):
    """Retrieves a NamedTensor by name.

    Args:
      name: Name of the tensor to retrieve.
      named_tensors: List of NamedTensor objects to search.

    Returns:
      The NamedTensor in |named_tensors| with the |name|.

    Raises:
      KeyError: If the |name| is not found among the |named_tensors|.
    """
    for named_tensor in named_tensors:
        if named_tensor.name == name:
            return named_tensor
    raise KeyError('Name "%s" not found in named tensors: %s' %
                   (name, named_tensors))


def activation_lookup_recurrent(component, state, channel_id, source_array,
                                source_layer_size, batch_size):
    """Looks up activations from tensor arrays.

    If the linked feature's embedding_dim is set to -1, the feature vectors are
    not passed through (i.e. multiplied by) an embedding matrix.

    Args:
      component: Component object in which to look up the fixed features.
      state: MasterState object for the live MasterState.
      channel_id: int id of the linked feature to look up.
      source_array: TensorArray from which to fetch feature vectors, expected to
          have size [steps + 1] elements of shape [batch_size, D] each.
      source_layer_size: int length of feature vectors before embedding.
      batch_size: int Tensor of current batch size.

    Returns:
      NamedTensor object containing the embedding vectors.
    """
    feature_spec = component.spec.linked_feature[channel_id]

    with tf.name_scope('activation_lookup_recurrent_%s' % feature_spec.name):
        # Linked features are returned as a pair of tensors, one indexing into
        # steps, and one indexing within the batch_size activation tensor
        # stored for a step.
        step_idx, idx = dragnn_ops.extract_link_features(
            state.handle, batch_size,
            component=component.name, channel_id=channel_id,
            channel_size=feature_spec.size)

        # We take the [steps, batch_size, ...] tensor array, gather and concat
        # the steps we might need into a [some_steps*batch_size, ...] tensor,
        # and flatten 'idx' to dereference this new tensor.
        #
        # The first element of each tensor array is reserved for an
        # initialization variable, so we offset all step indices by +1.
        #
        # TODO(googleuser): It would be great to not have to extract
        # the steps in their entirety, forcing a copy of much of the
        # TensorArray at each step. Better would be to support a
        # TensorArray.gather_nd to pick the specific elements directly.
        # TODO(googleuser): In the interim, a small optimization would
        # be to use tf.unique instead of tf.range.
        step_min = tf.reduce_min(step_idx)
        ta_range = tf.range(step_min + 1, tf.reduce_max(step_idx) + 2)
        act_block = source_array.gather(ta_range)
        act_block = tf.reshape(act_block,
                               tf.concat([[-1], tf.shape(act_block)[2:]], 0))
        flat_idx = (step_idx - step_min) * batch_size + idx
        act_block = tf.gather(act_block, flat_idx)
        act_block = tf.reshape(act_block, [-1, source_layer_size])

        if feature_spec.embedding_dim != -1:
            embedding_matrix = component.get_variable(
                linked_embeddings_name(channel_id))
            act_block = pass_through_embedding_matrix(act_block, embedding_matrix,
                                                      step_idx)
            dim = feature_spec.size * feature_spec.embedding_dim
        else:
            # If embedding_dim is -1, just output concatenation of activations.
            dim = feature_spec.size * source_layer_size

        return NamedTensor(
            tf.reshape(act_block, [-1, dim]), feature_spec.name, dim=dim)


def activation_lookup_other(component, state, channel_id, source_tensor,
                            source_layer_size, batch_size):
    """Looks up activations from tensors.

    If the linked feature's embedding_dim is set to -1, the feature vectors are
    not passed through (i.e. multiplied by) an embedding matrix.

    Args:
      component: Component object in which to look up the fixed features.
      state: MasterState object for the live MasterState.
      channel_id: int id of the linked feature to look up.
      source_tensor: Tensor from which to fetch feature vectors. Expected to have
          have shape [steps + 1, batch_size, D].
      source_layer_size: int length of feature vectors before embedding (D). It
          would in principle be possible to get this dimension dynamically from
          the second dimension of source_tensor. However, having it statically is
          more convenient.
      batch_size: int Tensor of current batch size.

    Returns:
      NamedTensor object containing the embedding vectors.
    """
    feature_spec = component.spec.linked_feature[channel_id]

    with tf.name_scope('activation_lookup_other_%s' % feature_spec.name):
        # Linked features are returned as a pair of tensors, one indexing into
        # steps, and one indexing within the stride (batch_size) of each step.
        step_idx, idx = dragnn_ops.extract_link_features(
            state.handle, batch_size,
            component=component.name, channel_id=channel_id,
            channel_size=feature_spec.size)

        # The first element of each tensor array is reserved for an
        # initialization variable, so we offset all step indices by +1.
        indices = tf.stack([step_idx + 1, idx], axis=1)
        act_block = tf.gather_nd(source_tensor, indices)
        act_block = tf.reshape(act_block, [-1, source_layer_size])

        if feature_spec.embedding_dim != -1:
            embedding_matrix = component.get_variable(
                linked_embeddings_name(channel_id))
            act_block = pass_through_embedding_matrix(act_block, embedding_matrix,
                                                      step_idx)
            dim = feature_spec.size * feature_spec.embedding_dim
        else:
            # If embedding_dim is -1, just output concatenation of activations.
            dim = feature_spec.size * source_layer_size

        return NamedTensor(
            tf.reshape(act_block, [-1, dim]), feature_spec.name, dim=dim)


class LayerNorm(object):
    """Utility to add layer normalization to any tensor.

    Layer normalization implementation is based on:

      https://arxiv.org/abs/1607.06450. "Layer Normalization"
      Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton

    This object will construct additional variables that need to be optimized, and
    these variables can be accessed via params().

    Attributes:
      params: List of additional parameters to be trained.
    """

    def __init__(self, component, name, shape, dtype):
        """Construct variables to normalize an input of given shape.

        Arguments:
          component: ComponentBuilder handle.
          name: Human readable name to organize the variables.
          shape: Shape of the layer to be normalized.
          dtype: Type of the layer to be normalized.
        """
        self._name = name
        self._shape = shape
        self._component = component
        beta = tf.get_variable(
            'beta_%s' % name,
            shape=shape,
            dtype=dtype,
            initializer=tf.zeros_initializer())
        gamma = tf.get_variable(
            'gamma_%s' % name,
            shape=shape,
            dtype=dtype,
            initializer=tf.ones_initializer())
        self._params = [beta, gamma]

    @property
    def params(self):
        return self._params

    def normalize(self, inputs):
        """Apply normalization to input.

        The shape must match the declared shape in the constructor.
        [This is copied from tf.contrib.rnn.LayerNormBasicLSTMCell.]

        Args:
          inputs: Input tensor

        Returns:
          Normalized version of input tensor.

        Raises:
          ValueError: if inputs has undefined rank.
        """
        inputs_shape = inputs.get_shape()
        inputs_rank = inputs_shape.ndims
        if inputs_rank is None:
            raise ValueError('Inputs %s has undefined rank.' % inputs.name)
        axis = range(1, inputs_rank)

        beta = self._component.get_variable('beta_%s' % self._name)
        gamma = self._component.get_variable('gamma_%s' % self._name)

        with tf.variable_scope('layer_norm_%s' % self._name):
            # Calculate the moments on the last axis (layer activations).
            mean, variance = nn.moments(inputs, axis, keep_dims=True)

            # Compute layer normalization using the batch_normalization function.
            variance_epsilon = 1E-12
            outputs = nn.batch_normalization(
                inputs, mean, variance, beta, gamma, variance_epsilon)
            outputs.set_shape(inputs_shape)
            return outputs


class Layer(object):
    """A layer in a feed-forward network.

    Attributes:
      component: ComponentBuilderBase that produces this layer.
      name: Name of this layer.
      dim: Dimension of this layer, or negative if dynamic.
    """

    def __init__(self, component, name, dim):
        check.NotNone(dim, 'Dimension is required')
        self.component = component
        self.name = name
        self.dim = dim

    def __str__(self):
        return 'Layer: %s/%s[%d]' % (self.component.name, self.name, self.dim)

    def create_array(self, stride):
        """Creates a new tensor array to store this layer's activations.

        Arguments:
          stride: Possibly dynamic batch size with which to initialize the
            tensor array

        Returns:
          TensorArray object
        """
        check.Gt(self.dim, 0, 'Cannot create array when dimension is dynamic')
        tensor_array = ta.TensorArray(dtype=tf.float32,
                                      size=0,
                                      dynamic_size=True,
                                      clear_after_read=False,
                                      infer_shape=False,
                                      name='%s_array' % self.name)

        # Start each array with all zeros. Special values will still be learned via
        # the extra embedding dimension stored for each linked feature channel.
        initial_value = tf.zeros([stride, self.dim])
        return tensor_array.write(0, initial_value)


def get_attrs_with_defaults(parameters, defaults):
    """Populates a dictionary with run-time attributes.

    Given defaults, populates any overrides from 'parameters' with their
    corresponding converted values. 'defaults' should be typed. This is useful
    for specifying NetworkUnit-specific configuration options.

    Args:
      parameters: a <string, string> map.
      defaults: a <string, value> typed set of default values.

    Returns:
      dictionary populated with any overrides.

    Raises:
      RuntimeError: if a key in parameters is not present in defaults.
    """
    attrs = defaults
    for key, value in parameters.items():
        check.In(key, defaults, 'Unknown attribute: %s' % key)
        if isinstance(defaults[key], bool):
            attrs[key] = value.lower() == 'true'
        else:
            attrs[key] = type(defaults[key])(value)
    return attrs


def maybe_apply_dropout(inputs, keep_prob, per_sequence, stride=None):
    """Applies dropout, if so configured, to an input tensor.

    The input may be rank 2 or 3 depending on whether the stride (i.e., batch
    size) has been incorporated into the shape.

    Args:
      inputs: [stride * num_steps, dim] or [stride, num_steps, dim] input tensor.
      keep_prob: Scalar probability of keeping each input element.  If >= 1.0, no
          dropout is performed.
      per_sequence: If true, sample the dropout mask once per sequence, instead of
          once per step.  Requires |stride| when true.
      stride: Scalar batch size.  Optional if |per_sequence| is false.

    Returns:
      [stride * num_steps, dim] or [stride, num_steps, dim] tensor, matching the
      shape of |inputs|, containing the masked or original inputs, depending on
      whether dropout was actually performed.
    """
    check.Ge(inputs.get_shape().ndims, 2, 'inputs must be rank 2 or 3')
    check.Le(inputs.get_shape().ndims, 3, 'inputs must be rank 2 or 3')
    flat = (inputs.get_shape().ndims == 2)

    if keep_prob >= 1.0:
        return inputs

    if not per_sequence:
        return tf.nn.dropout(inputs, keep_prob)

    check.NotNone(stride, 'per-sequence dropout requires stride')
    dim = inputs.get_shape().as_list()[-1]
    check.NotNone(dim, 'inputs must have static activation dimension, but have '
                       'static shape %s' % inputs.get_shape().as_list())

    # If needed, restore the batch dimension to separate the sequences.
    inputs_sxnxd = tf.reshape(inputs, [stride, -1, dim]) if flat else inputs

    # Replace |num_steps| with 1 in |noise_shape|, so the dropout mask broadcasts
    # to all steps for a particular sequence.
    noise_shape = [stride, 1, dim]
    masked_sxnxd = tf.nn.dropout(inputs_sxnxd, keep_prob, noise_shape)

    # If needed, flatten out the batch dimension in the return value.
    return tf.reshape(masked_sxnxd, [-1, dim]) if flat else masked_sxnxd


@registry.RegisteredClass
class NetworkUnitInterface(object):
    """Base class to implement NN specifications.

    This class contains the required functionality to build a network inside of a
    DRAGNN graph: (1) initializing TF variables during __init__(), and (2)
    creating particular instances from extracted features in create().

    Attributes:
      params (list): List of tf.Variable objects representing trainable
        parameters.
      layers (list): List of Layer objects to track network layers that should
        be written to Tensors during training and inference.
    """
    __metaclass__ = abc.ABCMeta  # required for @abstractmethod

    def __init__(self, component, init_layers=None, init_context_layers=None):
        """Initializes parameters for embedding matrices.

        The subclass may provide optional lists of initial layers and context layers
        to allow this base class constructor to use accessors like get_layer_size(),
        which is required for networks that may be used self-recurrently.

        Args:
          component: parent ComponentBuilderBase object.
          init_layers: optional initial layers.
          init_context_layers: optional initial context layers.
        """
        self._component = component
        self._params = []
        self._layers = init_layers if init_layers else []
        self._regularized_weights = []
        self._context_layers = init_context_layers if init_context_layers else []
        self._fixed_feature_dims = {}  # mapping from name to dimension
        self._linked_feature_dims = {}  # mapping from name to dimension
        self._fast_text_feature_dims = {}  # mapping from name to dimension

        # Allocate parameters for all embedding channels. Note that for both Fixed
        # and Linked embedding matrices, we store an additional +1 embedding that's
        # used when the index is out of scope.
        for channel_id, spec in enumerate(component.spec.fixed_feature):
            check.NotIn(spec.name, self._fixed_feature_dims,
                        'Duplicate fixed feature')
            if spec.embedding_dim > 0:
                fixed_dim = spec.embedding_dim
                self._params.append(add_embeddings(channel_id, spec))
            else:
                fixed_dim = 1  # assume feature ID extraction; only one ID per step
            self._fixed_feature_dims[spec.name] = fixed_dim

        for channel_id, spec in enumerate(component.spec.fast_text_feature):
            check.NotIn(spec.name, self._fast_text_feature_dims,
                        'Duplicate fixed feature')
            check.Gt(spec.embedding_dim, 0, 'Invalid fast text embedding_dim size')
            # we load fast text embeddings here
            dragnn_ops.word_embedding_initializer(vectors=spec.fast_text_model.part[0].file_pattern)
            self._fast_text_feature_dims[spec.name] = spec.embedding_dim

        for channel_id, spec in enumerate(component.spec.linked_feature):
            check.NotIn(spec.name, self._linked_feature_dims,
                        'Duplicate linked feature')
            check.Gt(spec.size, 0, 'Invalid linked feature size')

            if spec.source_component == component.name:
                source_array_dim = self.get_layer_size(spec.source_layer)
            else:
                source = component.master.lookup_component[spec.source_component]
                source_array_dim = source.network.get_layer_size(spec.source_layer)

            if spec.embedding_dim != -1:
                check.Gt(source_array_dim, 0,
                         'Cannot embed linked feature with dynamic dimension')
                self._params.append(
                    tf.get_variable(
                        linked_embeddings_name(channel_id),
                        [source_array_dim + 1, spec.embedding_dim],
                        initializer=tf.random_normal_initializer(
                            stddev=1 / spec.embedding_dim ** .5)))

                self._linked_feature_dims[spec.name] = spec.size * spec.embedding_dim
            else:
                # If embedding_dim is -1, linked features are not embedded.
                self._linked_feature_dims[spec.name] = spec.size * source_array_dim

        # Compute the cumulative dimension of all inputs.  If any input has dynamic
        # dimension, then the result is -1.
        input_dims = (list(self._fixed_feature_dims.values()) +
                      list(self._linked_feature_dims.values()) +
                      list(self._fast_text_feature_dims.values()))
        if any(x < 0 for x in input_dims):
            self._concatenated_input_dim = -1
        else:
            self._concatenated_input_dim = sum(input_dims)

        tf.logging.info('fixed features %s', self._fixed_feature_dims)
        tf.logging.info('fast text features %s', self._fast_text_feature_dims)
        tf.logging.info('linked features %s', self._linked_feature_dims)
        tf.logging.info('component %s concat_input_dim %s\n', component.name,
                        self._concatenated_input_dim)

    @abc.abstractmethod
    def create(self,
               fixed_embeddings,
               linked_embeddings,
               fast_text_embeddings,
               context_tensor_arrays,
               during_training,
               stride=None):
        """Constructs a feed-forward unit based on the features and context tensors.

        Args:
          fixed_embeddings: list of NamedTensor objects
          linked_embeddings: list of NamedTensor objects
          context_tensor_arrays: optional list of TensorArray objects used for
              implicit recurrence.
          during_training: whether to create a network for training (vs inference).
          stride: int scalar tensor containing the stride required for
              bulk computation.

        Returns:
          A list of tensors corresponding to the list of layers.
        """
        pass

    @property
    def layers(self):
        return self._layers

    @property
    def params(self):
        return self._params

    @property
    def regularized_weights(self):
        return self._regularized_weights

    @property
    def context_layers(self):
        return self._context_layers

    def get_layer_index(self, layer_name):
        """Gets the index of the given named layer of the network."""
        return [x.name for x in self.layers].index(layer_name)

    def get_layer_size(self, layer_name):
        """Gets the size of the given named layer of the network.

        Args:
          layer_name: string name of layer to look update

        Returns:
          the size of the layer.

        Raises:
          KeyError: if the layer_name to look up doesn't exist.
        """
        for layer in self.layers:
            if layer.name == layer_name:
                return layer.dim
        raise KeyError('Layer {} not found in component {}'.format(
            layer_name, self._component.name))

    def get_logits(self, network_tensors):
        """Pulls out the logits from the tensors produced by this unit.

        Args:
          network_tensors: list of tensors as output by create().

        Raises:
          NotImplementedError: by default a 'logits' tensor need not be implemented.
        """
        raise NotImplementedError()

    def get_l2_regularized_weights(self):
        """Gets the weights that need to be regularized."""
        return self.regularized_weights


class FeedForwardNetwork(NetworkUnitInterface):
    """Implementation of C&M style feedforward network.

    Supports dropout and optional layer normalization.

    Layers:
      layer_<i>: Activations for i'th hidden layer (0-origin).
      last_layer: Activations for the last hidden layer.  This is a convenience
          alias for "layer_<n-1>", where n is the number of hidden layers.
      logits: Logits associated with component actions.
    """

    def __init__(self, component):
        """Initializes parameters required to run this network.

        Args:
          component: parent ComponentBuilderBase object.

        Parameters used to construct the network:
          hidden_layer_sizes: comma-separated list of ints, indicating the
            number of hidden units in each hidden layer.
          layer_norm_input (False): Whether or not to apply layer normalization
            on the concatenated input to the network.
          layer_norm_hidden (False): Whether or not to apply layer normalization
            to the first set of hidden layer activations.
          nonlinearity ('relu'): Name of function from module "tf.nn" to apply to
            each hidden layer; e.g., "relu" or "elu".
          dropout_keep_prob (-1.0): The probability that an input is not dropped.
            If >= 1.0, disables dropout.  If < 0.0, uses the global |dropout_rate|
            hyperparameter.
          dropout_per_sequence (False): If true, sample the dropout mask once per
            sequence, instead of once per step.  See Gal and Ghahramani
            (https://arxiv.org/abs/1512.05287).
          dropout_all_layers (False): If true, apply dropout to the input of all
            hidden layers, instead of just applying it to the network input.

        Hyperparameters used:
          dropout_rate: The probability that an input is not dropped.  Only used
              when the |dropout_keep_prob| parameter is negative.
        """
        self._attrs = get_attrs_with_defaults(
            component.spec.network_unit.parameters, defaults={
                'hidden_layer_sizes': '',
                'layer_norm_input': False,
                'layer_norm_hidden': False,
                'nonlinearity': 'relu',
                'dropout_keep_prob': -1.0,
                'dropout_per_sequence': False,
                'dropout_all_layers': False})

        # Initialize the hidden layer sizes before running the base initializer, as
        # the base initializer may need to know the size of of the hidden layer for
        # recurrent connections.
        if self._attrs['hidden_layer_sizes']:
            self._hidden_layer_sizes = [int(x) for x in self._attrs['hidden_layer_sizes'].split(',')]
        else:
            self._hidden_layer_sizes = []

        super(FeedForwardNetwork, self).__init__(component)

        # Infer dropout rate from network parameters and grid hyperparameters.
        self._dropout_rate = self._attrs['dropout_keep_prob']
        if self._dropout_rate < 0.0:
            self._dropout_rate = component.master.hyperparams.dropout_rate

        # Add layer norm if specified.
        self._layer_norm_input = None
        self._layer_norm_hidden = None
        if self._attrs['layer_norm_input']:
            self._layer_norm_input = LayerNorm(self._component, 'concat_input',
                                               self._concatenated_input_dim,
                                               tf.float32)
            self._params.extend(self._layer_norm_input.params)

        if self._attrs['layer_norm_hidden']:
            self._layer_norm_hidden = LayerNorm(self._component, 'layer_0',
                                                self._hidden_layer_sizes[0],
                                                tf.float32)
            self._params.extend(self._layer_norm_hidden.params)

        # Extract nonlinearity from |tf.nn|.
        self._nonlinearity = getattr(tf.nn, self._attrs['nonlinearity'])

        # TODO(googleuser): add initializer stddevs as part of the network unit's
        # configuration.
        self._weights = []
        last_layer_dim = self._concatenated_input_dim

        # Initialize variables for the parameters, and add Layer objects for
        # cross-component bookkeeping.
        for index, hidden_layer_size in enumerate(self._hidden_layer_sizes):
            weights = tf.get_variable(
                'weights_%d' % index, [last_layer_dim, hidden_layer_size],
                initializer=tf.random_normal_initializer(stddev=1e-4))
            self._params.append(weights)
            if index > 0 or self._layer_norm_hidden is None:
                self._params.append(
                    tf.get_variable(
                        'bias_%d' % index, [hidden_layer_size],
                        initializer=tf.constant_initializer(
                            0.2, dtype=tf.float32)))

            self._weights.append(weights)
            self._layers.append(
                Layer(
                    component, name='layer_%d' % index, dim=hidden_layer_size))
            last_layer_dim = hidden_layer_size

        # Add a convenience alias for the last hidden layer, if any.
        if self._hidden_layer_sizes:
            self._layers.append(Layer(component, 'last_layer', last_layer_dim))

        # By default, regularize only the weights.
        self._regularized_weights.extend(self._weights)

        if component.num_actions:
            self._params.append(
                tf.get_variable(
                    'weights_softmax', [last_layer_dim, component.num_actions],
                    initializer=tf.random_normal_initializer(stddev=1e-4)))
            self._params.append(
                tf.get_variable(
                    'bias_softmax', [component.num_actions],
                    initializer=tf.zeros_initializer()))
            self._layers.append(
                Layer(
                    component, name='logits', dim=component.num_actions))

    def create(self,
               fixed_embeddings,
               linked_embeddings,
               fast_text_embeddings,
               context_tensor_arrays,
               during_training,
               stride=None):
        """See base class."""
        input_tensor = get_input_tensor(fixed_embeddings, linked_embeddings, fast_text_embeddings)

        if during_training:
            input_tensor.set_shape([None, self._concatenated_input_dim])
            input_tensor = self._maybe_apply_dropout(input_tensor, stride)

        if self._layer_norm_input:
            input_tensor = self._layer_norm_input.normalize(input_tensor)

        tensors = []
        last_layer = input_tensor
        for index, hidden_layer_size in enumerate(self._hidden_layer_sizes):
            acts = tf.matmul(last_layer,
                             self._component.get_variable('weights_%d' % index))

            # Note that the first layer was already handled before this loop.
            # TODO(googleuser): Refactor this loop so dropout and layer normalization
            # are applied consistently.
            if during_training and self._attrs['dropout_all_layers'] and index > 0:
                acts.set_shape([None, hidden_layer_size])
                acts = self._maybe_apply_dropout(acts, stride)

            # Don't add a bias term if we're going to apply layer norm, since layer
            # norm includes a bias already.
            if index == 0 and self._layer_norm_hidden:
                acts = self._layer_norm_hidden.normalize(acts)
            else:
                acts = tf.nn.bias_add(acts,
                                      self._component.get_variable('bias_%d' % index))

            last_layer = self._nonlinearity(acts)
            tensors.append(last_layer)

        # Add a convenience alias for the last hidden layer, if any.
        if self._hidden_layer_sizes:
            tensors.append(last_layer)

        if self._layers[-1].name == 'logits':
            logits = tf.matmul(
                last_layer, self._component.get_variable(
                    'weights_softmax')) + self._component.get_variable('bias_softmax')

            logits = tf.identity(logits, name=self._layers[-1].name)
            tensors.append(logits)
        return tensors

    def get_layer_size(self, layer_name):
        if layer_name == 'logits':
            return self._component.num_actions

        if layer_name == 'last_layer':
            return self._hidden_layer_sizes[-1]

        if not layer_name.startswith('layer_'):
            logging.fatal(
                'Invalid layer name: "%s" Can only retrieve from "logits", '
                '"last_layer", and "layer_*".',
                layer_name)

        # NOTE(danielandor): Since get_layer_size is called before the
        # model has been built, we compute the layer size directly from
        # the hyperparameters rather than from self._layers.
        layer_index = int(layer_name.split('_')[1])
        return self._hidden_layer_sizes[layer_index]

    def get_logits(self, network_tensors):
        return network_tensors[-1]

    def _maybe_apply_dropout(self, inputs, stride):
        return maybe_apply_dropout(inputs, self._dropout_rate,
                                   self._attrs['dropout_per_sequence'], stride)


class LSTMNetwork(NetworkUnitInterface):
    """Implementation of action LSTM style network."""

    def __init__(self, component):
        assert component.num_actions > 0, 'Component num actions must be positive.'
        network_unit_spec = component.spec.network_unit
        self._hidden_layer_sizes = (
            int)(network_unit_spec.parameters['hidden_layer_sizes'])

        self._input_dropout_rate = component.master.hyperparams.dropout_rate
        self._recurrent_dropout_rate = (
            component.master.hyperparams.recurrent_dropout_rate)
        if self._recurrent_dropout_rate < 0.0:
            self._recurrent_dropout_rate = component.master.hyperparams.dropout_rate

        super(LSTMNetwork, self).__init__(component)
        layer_input_dim = self._concatenated_input_dim

        self._context_layers = []

        # TODO(googleuser): should we choose different initilizer,
        # e.g. truncated_normal_initializer?
        self._x2i = tf.get_variable(
            'x2i', [layer_input_dim, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._h2i = tf.get_variable(
            'h2i', [self._hidden_layer_sizes, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._c2i = tf.get_variable(
            'c2i', [self._hidden_layer_sizes, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._bi = tf.get_variable(
            'bi', [self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))

        self._x2o = tf.get_variable(
            'x2o', [layer_input_dim, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._h2o = tf.get_variable(
            'h2o', [self._hidden_layer_sizes, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._c2o = tf.get_variable(
            'c2o', [self._hidden_layer_sizes, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._bo = tf.get_variable(
            'bo', [self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))

        self._x2c = tf.get_variable(
            'x2c', [layer_input_dim, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._h2c = tf.get_variable(
            'h2c', [self._hidden_layer_sizes, self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))
        self._bc = tf.get_variable(
            'bc', [self._hidden_layer_sizes],
            initializer=tf.random_normal_initializer(stddev=1e-4))

        self._params.extend([
            self._x2i, self._h2i, self._c2i, self._bi, self._x2o, self._h2o,
            self._c2o, self._bo, self._x2c, self._h2c, self._bc])

        lstm_h_layer = Layer(component, name='lstm_h', dim=self._hidden_layer_sizes)
        lstm_c_layer = Layer(component, name='lstm_c', dim=self._hidden_layer_sizes)

        self._context_layers.append(lstm_h_layer)
        self._context_layers.append(lstm_c_layer)

        self._layers.extend(self._context_layers)

        self._layers.append(
            Layer(component, name='layer_0', dim=self._hidden_layer_sizes))

        self.params.append(tf.get_variable(
            'weights_softmax', [self._hidden_layer_sizes, component.num_actions],
            initializer=tf.random_normal_initializer(stddev=1e-4)))
        self.params.append(
            tf.get_variable(
                'bias_softmax', [component.num_actions],
                initializer=tf.zeros_initializer()))

        self._layers.append(
            Layer(component, name='logits', dim=component.num_actions))

    def create(self,
               fixed_embeddings,
               linked_embeddings,
               fast_text_embeddings,
               context_tensor_arrays,
               during_training,
               stride=None):
        """See base class."""
        input_tensor = get_input_tensor(fixed_embeddings, linked_embeddings, fast_text_embeddings)

        # context_tensor_arrays[0] is lstm_h
        # context_tensor_arrays[1] is lstm_c
        assert len(context_tensor_arrays) == 2
        length = context_tensor_arrays[0].size()

        # Get the (possibly averaged) parameters to execute the network.
        x2i = self._component.get_variable('x2i')
        h2i = self._component.get_variable('h2i')
        c2i = self._component.get_variable('c2i')
        bi = self._component.get_variable('bi')
        x2o = self._component.get_variable('x2o')
        h2o = self._component.get_variable('h2o')
        c2o = self._component.get_variable('c2o')
        bo = self._component.get_variable('bo')
        x2c = self._component.get_variable('x2c')
        h2c = self._component.get_variable('h2c')
        bc = self._component.get_variable('bc')

        # i_h_tm1, i_c_tm1 = h_{t-1}, c_{t-1}
        i_h_tm1 = context_tensor_arrays[0].read(length - 1, name="lstm_h_in")
        i_c_tm1 = context_tensor_arrays[1].read(length - 1, name="lstm_c_in")

        # apply dropout according to http://arxiv.org/pdf/1409.2329v5.pdf
        if during_training and self._input_dropout_rate < 1:
            input_tensor = tf.nn.dropout(input_tensor, self._input_dropout_rate)

        # input --  i_t = sigmoid(affine(x_t, h_{t-1}, c_{t-1}))
        i_ait = tf.matmul(input_tensor, x2i) + tf.matmul(i_h_tm1, h2i) + tf.matmul(
            i_c_tm1, c2i) + bi
        i_it = tf.sigmoid(i_ait)

        # forget -- f_t = 1 - i_t
        i_ft = tf.ones([1, 1]) - i_it

        # write memory cell -- tanh(affine(x_t, h_{t-1}))
        i_awt = tf.matmul(input_tensor, x2c) + tf.matmul(i_h_tm1, h2c) + bc
        i_wt = tf.tanh(i_awt)

        # c_t = f_t \odot c_{t-1} + i_t \odot tanh(affine(x_t, h_{t-1}))
        ct = tf.add(
            tf.multiply(i_it, i_wt), tf.multiply(i_ft, i_c_tm1), name='lstm_c')

        # output -- o_t = sigmoid(affine(x_t, h_{t-1}, c_t))
        i_aot = tf.matmul(input_tensor, x2o) + tf.matmul(ct, c2o) + tf.matmul(
            i_h_tm1, h2o) + bo

        i_ot = tf.sigmoid(i_aot)

        # ht = o_t \odot tanh(ct)
        ph_t = tf.tanh(ct)
        ht = tf.multiply(i_ot, ph_t, name='lstm_h')

        if during_training and self._recurrent_dropout_rate < 1:
            ht = tf.nn.dropout(
                ht, self._recurrent_dropout_rate, name='lstm_h_dropout')

        h = tf.identity(ht, name='layer_0')

        logits = tf.nn.xw_plus_b(ht, tf.get_variable('weights_softmax'),
                                 tf.get_variable('bias_softmax'))

        logits = tf.identity(logits, name='logits')
        # tensors will be consistent with the layers:
        # [lstm_h, lstm_c, layer_0, logits]
        tensors = [ht, ct, h, logits]
        return tensors

    def get_layer_size(self, layer_name):
        assert layer_name == 'layer_0', 'Can only retrieve from first hidden layer.'
        return self._hidden_layer_sizes

    def get_logits(self, network_tensors):
        return network_tensors[self.get_layer_index('logits')]
