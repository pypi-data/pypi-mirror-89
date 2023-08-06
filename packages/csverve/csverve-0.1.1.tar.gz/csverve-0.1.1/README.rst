=======
csverve
=======


.. image:: https://img.shields.io/pypi/v/csverve.svg
        :target: https://pypi.python.org/pypi/csverve

.. image:: https://img.shields.io/travis/mondrian-scwgs/csverve.svg
        :target: https://travis-ci.com/mondrian-scwgs/csverve

.. image:: https://readthedocs.org/projects/csverve/badge/?version=latest
        :target: https://csverve.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Csverve, pronounced like "swerve" with a "v", is a package for manipulating tabular data.


* Free software: MIT license
* Documentation: https://csverve.readthedocs.io.


Features
--------

* Take in a regular gzipped CSV file and convert it to `csverve` format
* Merge gzipped CSZ files
* Concatenate gzipped CSV files (handles large datasets)
* Rewrite a gzipped CSV file (delete headers etc.)
* Annotate - add a column based on provided dictionary
* Write pandas DataFrame to `csverve` CSV
* Read a `csverve` CSV

Requirements
------------
Every gzipped CSV file must be accompanied by a meta YAML file. The meta yaml file must have the exact name as the
gzipped CSV file, with the addition of a `.yaml` ending.

csv.gz.yaml must contain:
=========================

* column names
* dtypes for each column
* separator
* header (bool) to specify if file has header or not

Example:

.. code-block:: yaml

   columns:
    - dtype: int
      name: prediction_id
    - dtype: str
      name: chromosome_1
    - dtype: str
      name: strand_1
    header: true
    sep: "\t"

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
