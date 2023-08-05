[![PyPI version](https://badge.fury.io/py/keras-sparsity-pattern.svg)](https://badge.fury.io/py/keras-sparsity-pattern)

# keras-sparsity-pattern
Tensorflow2/Keras wrapper for the `sparsity-pattern` package (DOI: [10.5281/zenodo.4357290](https://doi.org/10.5281/zenodo.4357290)).

## Installation
The `keras-sparsity-pattern` [git repo](http://github.com/ulf1/keras-sparsity-pattern) is available as [PyPi package](https://pypi.org/project/keras-sparsity-pattern)

```sh
pip install keras-sparsity-pattern
# pip install git+ssh://git@github.com/ulf1/keras-sparsity-pattern.git
```


## Usage
The `block`-diagonal pattern for tensorflow

```py
import keras_sparsity_pattern
import tensorflow as tf

n_rows, n_cols = 10, 12
mat_pattern = keras_sparsity_pattern.get('block', min(n_rows, n_cols), block_sizes=[3, 1, 2])
mat_values = range(1, len(mat_pattern)+1)

mat = tf.sparse.SparseTensor(
    dense_shape=(n_rows, n_cols),
    indices=mat_pattern,
    values=mat_values)

print(tf.sparse.to_dense(mat))
```

Please, check the [howto.ipynb of the sparsity-pattern package](https://github.com/ulf1/sparsity-pattern/blob/master/examples/howto.ipynb) for more sparsity patterns. 
The `.get` method works exactly the same.


## Appendix

### Install a virtual environment

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


### Support
Please [open an issue](https://github.com/ulf1/keras-sparsity-pattern/issues/new) for support.


### License and citation
This package is just a Keras wrapper for the python package [sparsity-pattern](https://github.com/ulf1/sparsity-pattern) what are both licensed under Apache License 2.0.
If you would like to cite the software, please use the `sparsity-pattern` package's DOI: [10.5281/zenodo.4357290](https://doi.org/10.5281/zenodo.4357290)


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/keras-sparsity-pattern/compare/).
