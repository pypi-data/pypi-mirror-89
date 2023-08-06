nnmnkwii (nanami)
=================

` <https://r9y9.github.io/nnmnkwii/stable>`__
` <https://r9y9.github.io/nnmnkwii/latest>`__
`PyPI <https://pypi.python.org/pypi/nnmnkwii>`__ `Build
Status <https://travis-ci.org/r9y9/nnmnkwii>`__ `Build
status <https://ci.appveyor.com/project/r9y9/nnmnkwii>`__ `Dependency
Status <https://dependencyci.com/github/r9y9/nnmnkwii>`__
`codecov <https://codecov.io/gh/r9y9/nnmnkwii>`__
`DOI <https://doi.org/10.5281/zenodo.1009252>`__

Library to build speech synthesis systems designed for easy and fast
prototyping.

Supported python versions: 2.7 and 3.6.

Documentation
-------------

-  `STABLE <https://r9y9.github.io/nnmnkwii/stable>`__ — **most recently
   tagged version of the documentation.**
-  `LATEST <https://r9y9.github.io/nnmnkwii/latest>`__ — *in-development
   version of the documentation.*

Installation
------------

The latest release is availabe on pypi. Assuming you have already
``numpy`` installed, you can install nnmnkwii by:

::

   pip install nnmnkwii

If you want the latest development version, run:

::

   pip install git+https://github.com/r9y9/nnmnkwii

or:

::

   git clone https://github.com/r9y9/nnmnkwii
   cd nnmnkwii
   python setup.py develop # or install

This should resolve the package dependencies and install ``nnmnkwii``
property.

At the moment, ``nnmnkwii.autograd`` package depends on
`PyTorch <http://pytorch.org/>`__. If you need autograd features, please
install PyTorch as well.

Acknowledgements
----------------

The library is inspired by the following open source projects:

-  Merlin: https://github.com/CSTR-Edinburgh/merlin
-  Librosa: https://github.com/librosa/librosa
