![CI](https://github.com/htseq/htseq/workflows/CI/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/htseq/badge/?version=master)](https://htseq.readthedocs.io)

# HTSeq
**DEVS**: https://github.com/htseq/htseq

**DOCS**: https://htseq.readthedocs.io

A Python library to facilitate processing and analysis of data
from high-throughput sequencing (HTS) experiments. A popular use of ``HTSeq``
is ``htseq-count``, a tool to quantify gene expression in RNA-Seq and similar
experiments.

## Requirements

To use ``HTSeq`` you will need:

-  ``Python >= 3.6`` (**note**: ``Python 2.7`` support has been dropped)
-  ``numpy``
-  ``pysam``

To run the ``htseq-qa`` script, you will also need:

-  ``matplotlib``

Both **Linux** and **OSX** are supported and binaries are provided on Pypi. We
would like to support **Windows** but currently lack the expertise to do so. If
you would like to take on the Windows release and maintenance, please open an
issue and we'll try to help.

A source package which should not require ``Cython`` nor ``SWIG`` is also
provided on Pypi.

To **develop** `HTSeq` you will **also** need:

-  ``Cython >=0.29.5``
-  ``SWIG >=3.0.8``

## Installation

### PIP

To install directly from PyPI:

```bash
pip install HTSeq
```

To install a specific version:

```bash
pip install 'HTSeq==0.14.0'
```

If this fails, please install all dependencies first:

```bash
pip install matplotlib
pip install Cython
pip install pysam
pip install HTSeq
```

### setup.py (distutils/setuptools)

Install the dependencies with your favourite tool (``pip``, ``conda``,
etc.).

To install ``HTSeq`` itself, run:

```bash
python setup.py build install
```

## Authors
- Since 2016: Fabio Zanini @ http://fabilab.org.
- 2020-2015: Simon Anders, Wolfgang Huber
