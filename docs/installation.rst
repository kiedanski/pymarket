.. highlight:: shell

============
Installation
============


Stable release
--------------

To install pymarket, run this command in your terminal:

First check your Python version, PyMarket requires Python 3.5.2 or newer.

.. code-block:: console
    
   $ python --version

Verify that pip is installed

.. code-block:: console   

   $ python -m pip --version

You can proceed to install PyMarket with the following command (the --user flag is optimal but recommended).

.. code-block:: console

    $ python -m pip install pymarket --user

This is the preferred method to install pymarket, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. warning::
    Python ` >=3.5.2 ` is required. PyMarket won't run with Python 2 nor previous versions of Python 3.


Dependencies
-------------

* PyMarket has been tested in Ubuntu 16.04, Ubuntu 18.04, Manjaro 18.1.1 and mac OS 10.14.4 (through travis only).
* PyMarket does not require additional dependencies outside for those specified in the `requeriments.txt` file. Nevertheless,
  `PulP` might benefit from having access to additional solvers such as CPLEX (not required).



From sources
------------

The sources for pymarket can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/gus0k/pymarket

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/gus0k/pymarket/tarball/master


Installing from source requires additional dependencies:

.. code-block:: console

      $ apt-get install --yes pkg-config
      $ apt-get install --yes libfreetype6-dev
      $ apt-get install --yes libpng12-dev
      $ python -m pip install 'setuptools>=27.3' --user


Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/gus0k/pymarket
.. _tarball: https://github.com/gus0k/pymarket/tarball/master


Running Tests
---------------

If the project was installed from source, in the main directory of the project run:

.. code-block:: console

        pytest

