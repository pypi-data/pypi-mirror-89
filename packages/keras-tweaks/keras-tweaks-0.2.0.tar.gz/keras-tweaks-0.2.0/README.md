[![PyPI version](https://badge.fury.io/py/keras-tweaks.svg)](https://badge.fury.io/py/keras-tweaks)

# keras-tweaks
Utility functions for Keras/Tensorflow2.


## Installation
The `keras-tweaks` [git repo](http://github.com/ulf1/keras-tweaks) is available as [PyPi package](https://pypi.org/project/keras-tweaks)

```sh
pip install keras-tweaks
# pip install git+ssh://git@github.com/ulf1/keras-tweaks.git
```


## Usage

### ID Sequence to Bool Mask

```py
import tensorflow as tf
from keras_tweaks import idseqs_to_mask

idseqs = [[1, 1, 0, 0, 2, 2, 3], [1, 3, 2, 1, 0, 0, 2]]

masks = idseqs_to_mask(
    idseqs, n_seqlen=6, ignore=[1],
    dtype=tf.uint8, dense=False)

print(tf.sparse.to_dense(masks))
```

See [example](http://github.com/ulf1/keras-tweaks/examples/help1.ipynb)


### Multiply row vector with sparse matrix
Please check the notebooks for [an example](http://github.com/ulf1/keras-tweaks/examples/dense_sparse_matmul-example.ipynb) and [an explanation](http://github.com/ulf1/keras-tweaks/examples/dense_sparse_matmul-explanation.ipynb)


```py
import tensorflow as tf
from keras_tweaks import dense_sparse_matmul

# 1x3 row vector
h = tf.constant([1., 2., 3.])

# 3x4 sparse matrix
W = tf.sparse.SparseTensor(
    indices=([0, 1], [1, 1], [1, 2], [2, 0], [2, 2], [0, 3], [2, 3]),
    values=[1., 2., 3., 4., 5., 6., 7.],
    dense_shape=(3, 4))
W = tf.sparse.reorder(W)

# result is a 1x4 row vector
net = dense_sparse_matmul(h, W)
```


### Sparsity Patterns for Keras
The `block`-diagonal pattern for tensorflow

```py
import tensorflow as tf
from keras_tweaks import get_sparsity_pattern

n_rows, n_cols = 10, 12
mat_pattern = get_sparsity_pattern('block', min(n_rows, n_cols), block_sizes=[3, 1, 2])
mat_values = range(1, len(mat_pattern)+1)

mat = tf.sparse.SparseTensor(
    dense_shape=(n_rows, n_cols),
    indices=mat_pattern,
    values=mat_values)

print(tf.sparse.to_dense(mat))
```

Please, check the [howto.ipynb of the sparsity-pattern package](https://github.com/ulf1/sparsity-pattern/blob/master/examples/howto.ipynb) for more sparsity patterns. 
The `keras_tweaks.get_sparsity_pattern` method works exactly the same.



## Appendix

### Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

### Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### License and citation
- The function `keras_tweaks.get_sparsity_pattern` is a wrapper for the python package [sparsity-pattern](https://github.com/ulf1/sparsity-pattern) what is also licensed under Apache License 2.0. If you are using the function, and like to cite the `sparsity-pattern` package, then use the DOI: [10.5281/zenodo.4357290](https://doi.org/10.5281/zenodo.4357290)


## Support
Please [open an issue](https://github.com/ulf1/keras-tweaks/issues/new) for support.


## Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/keras-tweaks/compare/).
