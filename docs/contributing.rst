============
Contributing
============

All project management tools are on GitHub:

- Bug tracking are in `issues`_
- Patches are submitted as `pull requests`_

Workflow
========

#. Fork project on GitHub.com
#. Make changes (and new unit tests if needed)
#. Ensure all tests are ok
#. Go to your fork and click on "Create pull request"

Tests
=====

All tests are simply launched by: ::

  python setup.py test

Or with coverage: ::

  coverage run setup.py test
  coverage html

Writing documentation
=====================

This documentation is built with `Sphinx`_, make your local docs with following
commands: ::

  make html
  cd _build/html
  python -m SimpleHTTPServer
 
Online resources
================

* `Code repository`_
* `Documentation`_
* `Travis CI server`_
* `Coveralls report`_
* `Landscape`_

.. _`issues`: https://github.com/ZuluPro/django-admin-cli/issues
.. _`pull requests`: https://github.com/ZuluPro/django-admin-cli/pulls
.. _`Sphinx`: http://sphinx-doc.org/
.. _`Code repository`: https://github.com/ZuluPro/django-admin-cli
.. _`Documentation`: https://github.com/ZuluPro/django-admin-cli#id3
.. _`Coveralls report`: https://coveralls.io/r/ZuluPro/django-admin-cli?branch=master
.. _`Travis CI server`: https://travis-ci.org/ZuluPro/django-admin-cli
.. _`Landscape`: https://landscape.io/github/ZuluPro/django-admin-cli/

