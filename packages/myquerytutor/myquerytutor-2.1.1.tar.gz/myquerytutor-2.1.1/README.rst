========
Overview
========

Educational tool to teach SQL

* Free software: GNU Lesser General Public License v3 or later (LGPLv3+)

Installation
============

::

    pip install myquerytutor



Documentation
=============


To use the project:

.. code-block:: python

    import myquerytutor
    myquerytutor.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
