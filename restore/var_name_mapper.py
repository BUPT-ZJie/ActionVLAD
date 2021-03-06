# ------------------------------------------------------------------------------
# ActionVLAD: Learning spatio-temporal aggregation for action classification
# Copyright (c) 2017 Carnegie Mellon University and Adobe Systems Incorporated
# Please see LICENSE on https://github.com/rohitgirdhar/ActionVLAD/ for details
# ------------------------------------------------------------------------------
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string(
  'var_name_mapping', 'none',
  'Map the variable names while loading caffemodels.')


def map():
  map_fn = lambda x: x
  if FLAGS.var_name_mapping == 'placenet365-vgg':
    map_fn = placenet365_vgg_fn
  elif FLAGS.var_name_mapping == 'cuhk-action-vgg':
    map_fn = cuhk_action_vgg
  elif FLAGS.var_name_mapping == 'cuhk-action-tsn':
    map_fn = cuhk_action_tsn
  elif FLAGS.var_name_mapping == 'xiaolonw_action_vgg_hmdb':
    map_fn = xiaolonw_action_vgg_hmdb
  return map_fn


def placenet365_vgg_fn(var_name):
  final_name = var_name
  if final_name.split('/')[0].startswith('conv'):
    final_name = \
      final_name.split('/')[0].split('_')[0] + '/' + final_name
  elif final_name.split('/')[0] == 'fc8a':
    final_name = final_name.replace('fc8a', 'fc8')
  return 'vgg_16/' + final_name + ':0'


def cuhk_action_vgg(var_name):
  final_name = var_name
  if final_name.split('/')[0].startswith('conv'):
    final_name = \
      final_name.split('/')[0].split('_')[0] + '/' + final_name
  elif final_name.split('/')[0].startswith('fc8'):
    final_name = final_name.replace(final_name.split('/')[0], 'fc8')
  return 'vgg_16/' + final_name + ':0'


def xiaolonw_action_vgg_hmdb(var_name):
  final_name = var_name
  if final_name.split('/')[0].startswith('conv'):
    final_name = \
      final_name.split('/')[0].split('_')[0] + '/' + final_name
  elif final_name.split('/')[0] == 'fc8_hmdb':
    final_name = final_name.replace('fc8_hmdb', 'fc8')
  return 'vgg_16/' + final_name + ':0'


def cuhk_action_tsn(var_name):
  final_name = var_name
  var_name = final_name.split('/')[-1]
  if final_name.split('/')[0].endswith('_bn'):
    if var_name == 'scale':
      var_name = 'gamma'
    elif var_name == 'shift':
      var_name = 'beta'
    elif var_name == 'mean':
      var_name = 'moving_mean'
    elif var_name == 'variance':
      var_name = 'moving_variance'
    final_name = \
      final_name.split('/')[0][:-3] + '/BatchNorm/' + var_name
  elif final_name.split('/')[0] == 'fc-action':
    final_name = 'Logits/Conv2d_1c_1x1/' + var_name
  else:
    final_name = final_name.split('/')[0] + '/Conv/' + var_name
  block_name = final_name.split('/')[0]
  pos = None
  if block_name.startswith('inception'):
    pos = len('inception_xx')
  elif block_name.startswith('conv'):
    pos = len('convx')
  if pos is not None:
    final_name = final_name[:pos] + '/' + final_name[pos+1:]
  return 'InceptionV2_TSN/' + final_name + ':0'
