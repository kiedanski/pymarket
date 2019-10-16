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
We recommend to have the latest version of pip available. To do so, run:

.. code-block:: console

   $ pip install --upgrade pip

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. warning::
    Python `3.6 >=` is required. PyMarket won't run on Python 2 nor Python 3.5.

Ubuntu 16.04 ships with Python 3.5. To update the python version do the following:

.. code-block:: console

        $ sudo add-apt-repository ppa:jonathonf/python-3.6
        $ sudo apt-get update
        $ sudo apt-get install python3.6
        $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1


Dependencies
-------------

* PyMarket has been tested in Ubuntu 16.04, Manjaro 18.1.1 and mac OS 10.14.4.
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
