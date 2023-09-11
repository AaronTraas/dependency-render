==================================================
dependency-render
==================================================

This renders a graph of dependencies. It takes as input a CSV called `dependencies.csv`, and uses Graphviz to generate a dependency map as a PDF.

==================================================
Installation
==================================================

This requires Python 3 and pip on your machine. To install, use

.. code::

  pip3 install dependency-render

If you have an older version installed, to upgrade to the latest version, run:

.. code::

  pip3 install -U dependency-render


==================================================
Syntax
==================================================

Usage:
.. code::
dependency-render [-h] [--output-type {pdf,png,svg}] [--debug] [--version] input_csv

positional arguments:
  `input_csv`: The CSV to parse

optional arguments:
  -h, --help           show this help message and exit
  --debug              Turns on debug mode
  --version            List the version of dependency-render.

Example:
```bash
python3 dependency-render.py dependencies.csv --output-type=svg
```

==================================================
CSV format
==================================================

It should be formatted with the following columns:

1. Application ID
2. Application Name
3. group
4. vendor
5. Availability SLO
6. Dependencies

--------------------------------------------------
Example
--------------------------------------------------

+----------------+------------------+-------+--------+------------------+---------------------------+
| Application ID | Application Name | group | vendor | Availability SLO | Dependencies              |
+----------------+------------------+-------+--------+------------------+---------------------------+
| foo            | Foo Application  |       |        | 0.99             | bar,baz,google-maps       |
+----------------+------------------+-------+--------+------------------+---------------------------+
| bar            | Bar API          | api   |        | 0.999            | mongo,okta                |
+----------------+------------------+-------+--------+------------------+---------------------------+
| baz            | Baz API          | api   |        | 0.999            | mongo,okta                |
+----------------+------------------+-------+--------+------------------+---------------------------+
| quux           | Quux API         | api   |        | 0.99             |                           |
+----------------+------------------+-------+--------+------------------+---------------------------+
| google-maps    | Google Maps API  |       | Google |                  |                           |
+----------------+------------------+-------+--------+------------------+---------------------------+
| okta           | Okta Core API    |       | Okta   |                  |                           |
+----------------+------------------+-------+--------+------------------+---------------------------+

See `example.csv` <./example.csv>`_.

The above will render to:

![Example graph](./example.svg)


==================================================
Development links
==================================================

This project uses SonarQube for static analysis. The results of analysis
are at `SonarCloud <AaronTraas_DependencyGenerator>`_.
The code quality and test coverage are a work in progress.
