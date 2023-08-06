.. image:: https://travis-ci.org/hapi-server/client-python.svg?branch=master
    :target: https://travis-ci.org/hapi-server/client-python

HAPI client for Python 2/3
==============================

Installation
------------

.. code:: bash

    pip install hapiclient --upgrade
    # or
    pip install 'git+https://github.com/hapi-server/client-python' --upgrade

See the `Appendix <#Appendix>`__ for a fail-safe installation method.

Basic Example
-------------

.. code:: python

    # Get and plot Dst index from CDAWeb HAPI server
    from hapiclient import hapi
    from hapiclient import hapiplot

    server     = 'https://cdaweb.gsfc.nasa.gov/hapi'
    dataset    = 'OMNI2_H0_MRG1HR'
    start      = '2003-09-01T00:00:00'
    stop       = '2003-12-01T00:00:00'
    parameters = 'DST1800'
    opts       = {'logging': True}

    # Get data
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    # Show documentation
    #help(hapi)

    # Plot all parameters
    hapiplot(data, meta)
    # Show documentation
    #help(hapiplot)

Documentation
-------------

Basic usage examples for various HAPI servers are given in `hapi_demo.py <https://github.com/hapi-server/client-python/blob/master/hapi_demo.py>`__

All of the features are extensively demonstrated in the `hapi_demo.ipynb <https://github.com/hapi-server/client-python-notebooks/blob/master/hapi_demo.ipynb>`__ Jupyter Notebook.

Development
-----------

.. code:: bash

    git clone https://github.com/hapi-server/client-python
    cd client-python; python setup.py develop

(The command python setup.py develop creates symlinks so that the local package is
used instead of an installed package. You may need to execute ``pip uninstall hapiclient`` 
first to ensure the local package is used.)

To run tests before a commit, execute

.. code:: bash

    make repository-test

To run an individual unit test in a Python session, use, e.g.,

.. code:: python

    from hapiclient.test.test_hapi import test_reader_short
    test_reader_short()

Contact
-------

Submit bug reports and feature requests on the `repository issue
tracker <https://github.com/hapi-server/client-python/issues>`__.

Appendix
--------

Fail-safe installation

Python command line:

.. code:: python

    import os
    print(os.popen("pip install hapiclient").read())

The above executes and displays the output of the operating system
command ``pip install hapiclient`` using the shell environment
associated with that installation of Python.

This method addresses a problem that is sometimes encountered when
attempting to use ``pip`` packages in Anaconda. To use a ``pip`` package
in Anaconda, one must use the version of ``pip`` installed with Anaconda
(it is usually under a subdirectory with the name ``anaconda/``) as
opposed to the one installed with the operating system. To see the
location of ``pip`` used in a given Python session, enter
``print(os.popen("which pip").read())``.
