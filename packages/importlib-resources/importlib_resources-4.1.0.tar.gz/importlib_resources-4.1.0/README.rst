.. image:: https://img.shields.io/pypi/v/skeleton.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/skeleton.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/skeleton

.. image:: https://github.com/jaraco/skeleton/workflows/Automated%20Tests/badge.svg
   :target: https://github.com/jaraco/skeleton/actions?query=workflow%3A%22Automated+Tests%22
   :alt: Automated Tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

``importlib_resources`` is a backport of Python standard library
`importlib.resources
<https://docs.python.org/3/library/importlib.html#module-importlib.resources>`_
module for older Pythons.  Users of Python 3.9 and beyond
should use the standard library module, since for these versions,
``importlib_resources`` just delegates to that module.

The key goal of this module is to replace parts of `pkg_resources
<https://setuptools.readthedocs.io/en/latest/pkg_resources.html>`_ with a
solution in Python's stdlib that relies on well-defined APIs.  This makes
reading resources included in packages easier, with more stable and consistent
semantics.
