# Pandas pipeline in graphviz

Python package to build a nice explanative schema of a data processing pipeline in pandas.

It's heavily inspired by dask's [`.visualize` method](https://docs.dask.org/en/latest/graphviz.html), but improved with 2 useful features:
- visualize columns names in data nodes
- highlight created columns at each task

## Installation

### Pip

Install with pip:
```bash
$ pip install pandas-pipeline-graphviz
```

### Manual installation

Install manually:
- git clone
- use `python setup.py`

## Usage

### Disclaimer: it's a hack

**⚠️ WARNING: Hack!**

There are no reliable methods to get variables names, either as input, or as output are quite hacky, as shown in this [stackoverflow thread about "How to get the original variable name of variable passed to a function"](https://stackoverflow.com/questions/2749796/how-to-get-the-original-variable-name-of-variable-passed-to-a-function).

To build the graph, this packages makes use of:
- to get the names of input dataframes: the package uses `globals()`, doing a comparison between the input dataframes and all the variables available in the global variables.
- to detect output dataframe name: the package uses `inspect.stack()`, gathering the code lines calling the function and parsing it to find the output. Currently it supports only single-output transformations.

Both methods should be considered as experimental and the behavior of the decorator is expected to break easily if it's not used as presented in the example.

### Conditions for use:

- do not use several decorators on your function, only this decorator, otherwise it will break the output dataframe name detection through `inspect.stack()`
- use only single output transformation functions, i.e. function which return only 1 dataframe.

### Example

See [examples folder](examples) in the repository.
