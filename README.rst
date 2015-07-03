================
Django Admin CLI
================

.. image :: https://travis-ci.org/ZuluPro/django-admin-cli.svg?branch=master
    :target: https://travis-ci.org/ZuluPro/django-admin-cli

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
