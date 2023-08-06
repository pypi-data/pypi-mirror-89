Django AWS Utils
================

|Docs badge| |Style badge| |License badge|

This is a package of utilities that aim to help with Django deployment on AWS.

Usage
-----

See `the main documentation site <http://django-aws-utils.rtfd.io/>`_ for details.

The package is available on PyPI.

.. code-block::

    pip install django-aws-utils

Then import the functions you need:

.. code-block::

    from django_aws_utils import get_ec2_ip

    ALLOWED_HOSTS = [
        get_ec2_ip(),
        "myapp.my.domain.com",
    ]

License
-------

This project is released under the terms of the "New" BSD 3-Clause license.
Please see `LICENSE <LICENSE>`_ for the full licence text.

.. |Style badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
.. |License badge| image:: https://img.shields.io/github/license/vladvasiliu/django-aws-utils.svg
   :target: LICENSE
.. |Docs badge| image:: https://readthedocs.org/projects/django-aws-utils/badge/?version=latest
   :target: https://django-aws-utils.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
