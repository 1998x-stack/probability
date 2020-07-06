<div itemscope itemtype="http://developers.google.com/ReferenceObject">
<meta itemprop="name" content="tfp.edward2.Kumaraswamy" />
<meta itemprop="path" content="Stable" />
</div>

# tfp.edward2.Kumaraswamy


<table class="tfo-notebook-buttons tfo-api" align="left">

<td>
  <a target="_blank" href="https://github.com/tensorflow/probability/blob/master/tensorflow_probability/python/experimental/edward2/interceptor.py">
    <img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />
    View source on GitHub
  </a>
</td></table>



Create a random variable for Kumaraswamy.

### Aliases:

* `tfp.experimental.edward2.Kumaraswamy`


``` python
tfp.edward2.Kumaraswamy(
    *args,
    **kwargs
)
```



<!-- Placeholder for "Used in" -->

See Kumaraswamy for more details.

#### Returns:

RandomVariable.


#### Original Docstring for Distribution

Initialize a batch of Kumaraswamy distributions.

#### Args:


* <b>`concentration1`</b>: Positive floating-point `Tensor` indicating mean
  number of successes; aka "alpha". Implies `self.dtype` and
  `self.batch_shape`, i.e.,
  `concentration1.shape = [N1, N2, ..., Nm] = self.batch_shape`.
* <b>`concentration0`</b>: Positive floating-point `Tensor` indicating mean
  number of failures; aka "beta". Otherwise has same semantics as
  `concentration1`.
* <b>`validate_args`</b>: Python `bool`, default `False`. When `True` distribution
  parameters are checked for validity despite possibly degrading runtime
  performance. When `False` invalid inputs may silently render incorrect
  outputs.
* <b>`allow_nan_stats`</b>: Python `bool`, default `True`. When `True`, statistics
  (e.g., mean, mode, variance) use the value "`NaN`" to indicate the
  result is undefined. When `False`, an exception is raised if one or
  more of the statistic's batch members are undefined.
* <b>`name`</b>: Python `str` name prefixed to Ops created by this class.