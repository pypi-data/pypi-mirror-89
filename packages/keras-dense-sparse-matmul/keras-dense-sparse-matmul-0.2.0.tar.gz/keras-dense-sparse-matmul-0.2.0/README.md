[![PyPI version](https://badge.fury.io/py/keras-dense-sparse-matmul.svg)](https://badge.fury.io/py/keras-dense-sparse-matmul)

# keras-dense-sparse-matmul
This package only contains one utility function `dense_sparse_matmul` to multiply a (dense) row vector with sparse matrix in tensorflow.


## Installation
The `keras-dense-sparse-matmul` [git repo](http://github.com/ulf1/keras-dense-sparse-matmul) is available as [PyPi package](https://pypi.org/project/keras-dense-sparse-matmul)

```sh
pip install keras-dense-sparse-matmul
# pip install git+ssh://git@github.com/ulf1/keras-dense-sparse-matmul.git
```

## Usage

```py
import tensorflow as tf
from keras_dense_sparse_matmul import dense_sparse_matmul

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

Check the [example notebook](http://github.com/ulf1/keras-dense-sparse-matmul/examples/example.ipynb).


## Appendix

### Install in a virtual environment
If you want to check the function `dense_sparse_matmul` first, 
you can use Binder or install a virtual environment on your local computer

```
python3.6 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
pip3 install -r requirements-demo.txt
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands
* Activate the virtual env: `source .venv/bin/activate`
* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

### Clean up commands

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```

### Support
Please [open an issue](https://github.com/ulf1/keras-dense-sparse-matmul/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/keras-dense-sparse-matmul/compare/).
