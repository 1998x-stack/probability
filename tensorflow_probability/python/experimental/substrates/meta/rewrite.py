# Copyright 2019 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Rewrite script for TF->JAX."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

# Dependency imports
from absl import app
from absl import flags

flags.DEFINE_boolean('numpy_to_jax', False,
                     'Whether or not to rewrite numpy imports to jax.numpy')

FLAGS = flags.FLAGS

TF_REPLACEMENTS = {
    'import tensorflow ':
        'from tensorflow_probability.python.internal.backend import numpy ',
    'import tensorflow.compat.v1':
        'from tensorflow_probability.python.internal.backend.numpy.compat '
        'import v1',
    'import tensorflow.compat.v2':
        'from tensorflow_probability.python.internal.backend.numpy.compat '
        'import v2',
    'import tensorflow_probability as tfp':
        'import tensorflow_probability as tfp; '
        'tfp = tfp.experimental.substrates.numpy',
}

DISABLED_BIJECTORS = ('masked_autoregressive', 'scale_matvec_lu', 'real_nvp')
DISABLED_DISTS = ('joint_distribution',
                  'internal.moving_stats', 'student_t_process',
                  'variational_gaussian_process')
LIBS = ('bijectors', 'distributions',
        'math', 'math.psd_kernels', 'math.psd_kernels.internal',
        'stats',
        'util', 'util.seed_stream', 'util.deferred_tensor')
INTERNALS = ('assert_util', 'distribution_util', 'dtype_util',
             'hypothesis_testlib', 'prefer_static', 'special_math',
             'tensor_util', 'test_combinations', 'test_util')


def main(argv):

  replacements = collections.OrderedDict(TF_REPLACEMENTS)
  replacements.update({
      'from tensorflow_probability.python.bijectors.{}'.format(bijector):
      '# from tensorflow_probability.python.bijectors.{}'.format(bijector)
      for bijector in DISABLED_BIJECTORS
  })
  if not FLAGS.numpy_to_jax:
    disabled_dists = DISABLED_DISTS + ('gaussian_process',)
  else:
    disabled_dists = DISABLED_DISTS
  replacements.update({
      'from tensorflow_probability.python.distributions.{}'.format(dist):
      '# from tensorflow_probability.python.distributions.{}'.format(dist)
      for dist in disabled_dists
  })
  substrates_pkg = 'tensorflow_probability.python.experimental.substrates'
  replacements.update({
      'tensorflow_probability.python.{}'.format(lib):
      '{}.numpy.{}'.format(substrates_pkg, lib)
      for lib in LIBS
  })
  replacements.update({
      'tensorflow_probability.python import {}'.format(lib):
      '{}.numpy import {}'.format(substrates_pkg, lib)
      for lib in LIBS
  })
  replacements.update({
      'tensorflow_probability.python.internal.{}'.format(internal):
      '{}.numpy.internal.{}'.format(substrates_pkg, internal)
      for internal in INTERNALS
  })
  replacements.update({
      'tensorflow_probability.python.internal import {}'.format(internal):
      '{}.numpy.internal import {}'.format(substrates_pkg, internal)
      for internal in INTERNALS
  })
  replacements.update({
      'self._maybe_assert_dtype': '# self._maybe_assert_dtype',
      'SKIP_DTYPE_CHECKS = False': 'SKIP_DTYPE_CHECKS = True',
      '@test_util.test_all_tf_execution_regimes': (
          '# @test_util.test_all_tf_execution_regimes'),
      '@test_util.test_graph_and_eager_modes': (
          '# @test_util.test_graph_and_eager_modes'),
      'TestCombinationsTest(test_util.TestCase)': (
          'TestCombinationsDoNotTest(object)')
  })

  contents = open(argv[1]).read()
  for find, replace in replacements.items():
    contents = contents.replace(find, replace)
  if FLAGS.numpy_to_jax:
    contents = contents.replace('substrates.numpy', 'substrates.jax')
    contents = contents.replace('substrates import numpy',
                                'substrates import jax')
    contents = contents.replace('backend.numpy', 'backend.jax')
    contents = contents.replace('backend import numpy', 'backend import jax')
    contents = contents.replace('def _call_jax', 'def __call__')
    contents = contents.replace('JAX_MODE = False', 'JAX_MODE = True')
    contents = contents.replace('SKIP_DTYPE_CHECKS = True',
                                'SKIP_DTYPE_CHECKS = False')
    is_test = lambda x: x.endswith('_test.py') or x.endswith('_test_util.py')
    if not is_test(argv[1]):  # We leave tests with original np.
      contents = contents.replace(
          '\nimport numpy as np',
          '\nimport numpy as onp\nimport jax.numpy as np')
      contents = contents.replace('np.generic', 'onp.generic')
      contents = contents.replace('np.bool', 'onp.bool')
      contents = contents.replace('np.dtype', 'onp.dtype')
      contents = contents.replace('np.unique', 'onp.unique')
      contents = contents.replace('np.euler_gamma', 'onp.euler_gamma')
      contents = contents.replace('np.nextafter', 'onp.nextafter')
    if is_test(argv[1]):  # Test-only rewrites.
      contents = contents.replace(
          'tf.test.main()',
          'from jax.config import config; '
          'config.update("jax_enable_x64", True); '
          'tf.test.main()')

  print(contents)


if __name__ == '__main__':
  app.run(main)
