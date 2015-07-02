================
Django Admin CLI
================

.. image :: https://travis-ci.org/ZuluPro/django-admin-cli.svg?branch=master
   :target: https://travis-ci.org/ZuluPro/django-admin-cli
    
.. image:: https://coveralls.io/repos/ZuluPro/django-admin-cli/badge.svg?branch=master
   :target: https://coveralls.io/r/ZuluPro/django-admin-cli?branch=master

.. image:: https://landscape.io/github/ZuluPro/django-admin-cli/master/landscape.svg?style=flat
   :target: https://landscape.io/github/ZuluPro/django-admin-cli/master
   :alt: Code Health

Django third app for manage you models in command line environment.

.. contents:: **Table of content**

Features
========

This app is based on Django Admin Site and ModelAdmin defined by developpers.
It is supposed to allow user to make same things as in Admin site:

- List model's instance:

  * Filtering with Django's Lookup
  * Choosing which field you want including ModelAdmin and Model attributes
  * Default display is the Admin one
  
- Add an instance:

  * Prepopulate with default values
  
- Update instances:

  * Filtering with Django's Lookup
  
- Delete instances:

  * Filtering with Django's Lookup

- Describe model and modeladmin
- Use admin actions (further)

Install
=======

Install the package on your system: ::

    pip install django-admin-cli

Add ``admin_cli`` to ``INSTALLED_APPS``.

Usage
=====

List model's instance
---------------------

::

  $ ./manage.py cli user list
  Username                      Email address                 First name                    Last name                     Staff status
  zulu                                                                                                                    True
  admin                                                                                                                   True
    
List specified fields
---------------------

::

  $ ./manage.py cli user list -f id -f username
  Id                   Username
  1                    zulu
  2                    admin

Filter specified fields
-----------------------

::

  $ ./manage.py cli user list -F id=1
  Username                      Email address                 First name                    Last name                     Staff status
  zulu                                                                                                                    True

Add an instance
---------------

::

  $ ./manage.py cli site add -f domain=mysite.org -f 'name=My site'
  Created 'mysite.org'

Update an instance
------------------

::

  $ ./manage.py cli site update -F domain=mysite.org -f 'name=New name'
  Update 'mysite.org' ? [Yes|No|All|Cancel] y
  Updated 'mysite.org'

Delete an instance
------------------

::

  $ ./manage.py cli site delete -F domain=mysite.org
  Delete 'mysite.org' ? [Yes|No|All|Cancel] y
  Deleted 'mysite.org'

Testing
=======

All tests are simply launched by:

::

  python setup.py test

Online resources
================

* `Code repository`_
* `Documentation`_
* `Travis CI server`_
* `Coveralls report`_
* `Landscape`

.. _`Code repository`: https://github.com/ZuluPro/django-admin-cli
.. _`Documentation`: https://github.com/ZuluPro/django-admin-cli#id3
.. _`Coveralls report`: https://coveralls.io/r/ZuluPro/django-admin-cli?branch=master
.. _`Travis CI server`: https://travis-ci.org/ZuluPro/django-admin-cli
.. _`Landscape`: https://landscape.io/github/ZuluPro/django-admin-cli/
