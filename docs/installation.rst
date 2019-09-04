.. highlight:: shell

============
Installation
============


Stable release
--------------

To install pymarket, run this command in your terminal:

.. code-block:: console

    $ pip install pymarket

This is the preferred method to install pymarket, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. warning::
    Python `3.6 >=` is required. PyMarket won't run on Python 2.

Dependencies
-------------

* PyMarket has been tested in Linux and mac OS.
* Python `3.6 >=` is required. The code currently uses `f-strings` only introduced in python version 3.6.
* Versions `3.6, 3.7` have been tested and are working.
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

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/gus0k/pymarket
.. _tarball: https://github.com/gus0k/pymarket/tarball/master


Running Tests
---------------

If the project was installed from source:

.. code-block:: console

    pip install --user -r requirements_dev.txt
    make test

And to check the coverage

.. code-block:: console
    make coverage
