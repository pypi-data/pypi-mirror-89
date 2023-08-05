# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator/create_python_api.py script.
"""Wrappers for primitive Neural Net (NN) Operations.
"""

from __future__ import print_function as _print_function

import sys as _sys

from tensorflow._api.v1.compat.v1.nn import rnn_cell
from tensorflow.python.ops.array_ops import depth_to_space
from tensorflow.python.ops.array_ops import space_to_batch
from tensorflow.python.ops.array_ops import space_to_depth
from tensorflow.python.ops.candidate_sampling_ops import all_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import compute_accidental_hits
from tensorflow.python.ops.candidate_sampling_ops import fixed_unigram_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import learned_unigram_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import log_uniform_candidate_sampler
from tensorflow.python.ops.candidate_sampling_ops import uniform_candidate_sampler
from tensorflow.python.ops.ctc_ops import collapse_repeated
from tensorflow.python.ops.ctc_ops import ctc_beam_search_decoder
from tensorflow.python.ops.ctc_ops import ctc_beam_search_decoder_v2
from tensorflow.python.ops.ctc_ops import ctc_greedy_decoder
from tensorflow.python.ops.ctc_ops import ctc_loss
from tensorflow.python.ops.ctc_ops import ctc_loss_v2
from tensorflow.python.ops.ctc_ops import ctc_unique_labels
from tensorflow.python.ops.embedding_ops import embedding_lookup
from tensorflow.python.ops.embedding_ops import embedding_lookup_sparse
from tensorflow.python.ops.embedding_ops import safe_embedding_lookup_sparse
from tensorflow.python.ops.gen_math_ops import tanh
from tensorflow.python.ops.gen_nn_ops import conv3d_backprop_filter_v2
from tensorflow.python.ops.gen_nn_ops import conv3d_backprop_filter_v2 as conv3d_backprop_filter
from tensorflow.python.ops.gen_nn_ops import depthwise_conv2d_native
from tensorflow.python.ops.gen_nn_ops import depthwise_conv2d_native_backprop_filter
from tensorflow.python.ops.gen_nn_ops import depthwise_conv2d_native_backprop_filter as depthwise_conv2d_backprop_filter
from tensorflow.python.ops.gen_nn_ops import depthwise_conv2d_native_backprop_input
from tensorflow.python.ops.gen_nn_ops import depthwise_conv2d_native_backprop_input as depthwise_conv2d_backprop_input
from tensorflow.python.ops.gen_nn_ops import elu
from tensorflow.python.ops.gen_nn_ops import l2_loss
from tensorflow.python.ops.gen_nn_ops import lrn
from tensorflow.python.ops.gen_nn_ops import lrn as local_response_normalization
from tensorflow.python.ops.gen_nn_ops import quantized_avg_pool
from tensorflow.python.ops.gen_nn_ops import quantized_conv2d
from tensorflow.python.ops.gen_nn_ops import quantized_max_pool
from tensorflow.python.ops.gen_nn_ops import quantized_relu_x
from tensorflow.python.ops.gen_nn_ops import relu
from tensorflow.python.ops.gen_nn_ops import selu
from tensorflow.python.ops.gen_nn_ops import softplus
from tensorflow.python.ops.gen_nn_ops import softsign
from tensorflow.python.ops.math_ops import sigmoid
from tensorflow.python.ops.nn_impl import batch_norm_with_global_normalization
from tensorflow.python.ops.nn_impl import batch_normalization
from tensorflow.python.ops.nn_impl import compute_average_loss
from tensorflow.python.ops.nn_impl import depthwise_conv2d
from tensorflow.python.ops.nn_impl import fused_batch_norm
from tensorflow.python.ops.nn_impl import l2_normalize
from tensorflow.python.ops.nn_impl import log_poisson_loss
from tensorflow.python.ops.nn_impl import moments
from tensorflow.python.ops.nn_impl import nce_loss
from tensorflow.python.ops.nn_impl import normalize_moments
from tensorflow.python.ops.nn_impl import relu_layer
from tensorflow.python.ops.nn_impl import sampled_softmax_loss
from tensorflow.python.ops.nn_impl import scale_regularization_loss
from tensorflow.python.ops.nn_impl import separable_conv2d
from tensorflow.python.ops.nn_impl import sigmoid_cross_entropy_with_logits
from tensorflow.python.ops.nn_impl import sufficient_statistics
from tensorflow.python.ops.nn_impl import swish
from tensorflow.python.ops.nn_impl import weighted_cross_entropy_with_logits
from tensorflow.python.ops.nn_impl import weighted_moments
from tensorflow.python.ops.nn_impl import zero_fraction
from tensorflow.python.ops.nn_ops import atrous_conv2d
from tensorflow.python.ops.nn_ops import atrous_conv2d_transpose
from tensorflow.python.ops.nn_ops import avg_pool
from tensorflow.python.ops.nn_ops import avg_pool as avg_pool2d
from tensorflow.python.ops.nn_ops import avg_pool1d
from tensorflow.python.ops.nn_ops import avg_pool3d
from tensorflow.python.ops.nn_ops import avg_pool_v2
from tensorflow.python.ops.nn_ops import bias_add
from tensorflow.python.ops.nn_ops import conv1d
from tensorflow.python.ops.nn_ops import conv1d_transpose
from tensorflow.python.ops.nn_ops import conv2d
from tensorflow.python.ops.nn_ops import conv2d_backprop_filter
from tensorflow.python.ops.nn_ops import conv2d_backprop_input
from tensorflow.python.ops.nn_ops import conv2d_transpose
from tensorflow.python.ops.nn_ops import conv3d_transpose
from tensorflow.python.ops.nn_ops import conv3d_v1 as conv3d
from tensorflow.python.ops.nn_ops import conv_transpose
from tensorflow.python.ops.nn_ops import convolution
from tensorflow.python.ops.nn_ops import crelu
from tensorflow.python.ops.nn_ops import dilation2d_v1 as dilation2d
from tensorflow.python.ops.nn_ops import dropout
from tensorflow.python.ops.nn_ops import erosion2d
from tensorflow.python.ops.nn_ops import fractional_avg_pool
from tensorflow.python.ops.nn_ops import fractional_max_pool
from tensorflow.python.ops.nn_ops import in_top_k
from tensorflow.python.ops.nn_ops import leaky_relu
from tensorflow.python.ops.nn_ops import log_softmax
from tensorflow.python.ops.nn_ops import max_pool
from tensorflow.python.ops.nn_ops import max_pool1d
from tensorflow.python.ops.nn_ops import max_pool2d
from tensorflow.python.ops.nn_ops import max_pool3d
from tensorflow.python.ops.nn_ops import max_pool_v2
from tensorflow.python.ops.nn_ops import max_pool_with_argmax_v1 as max_pool_with_argmax
from tensorflow.python.ops.nn_ops import pool
from tensorflow.python.ops.nn_ops import relu6
from tensorflow.python.ops.nn_ops import softmax
from tensorflow.python.ops.nn_ops import softmax_cross_entropy_with_logits
from tensorflow.python.ops.nn_ops import softmax_cross_entropy_with_logits_v2_helper as softmax_cross_entropy_with_logits_v2
from tensorflow.python.ops.nn_ops import sparse_softmax_cross_entropy_with_logits
from tensorflow.python.ops.nn_ops import top_k
from tensorflow.python.ops.nn_ops import with_space_to_batch
from tensorflow.python.ops.nn_ops import xw_plus_b
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn
from tensorflow.python.ops.rnn import dynamic_rnn
from tensorflow.python.ops.rnn import raw_rnn
from tensorflow.python.ops.rnn import static_bidirectional_rnn
from tensorflow.python.ops.rnn import static_rnn
from tensorflow.python.ops.rnn import static_state_saving_rnn

del _print_function

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "compat.v1.nn", public_apis=None, deprecation=False,
      has_lite=False)
