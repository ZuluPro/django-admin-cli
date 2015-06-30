================
Django Admin CLI
================

Django third app for manage you models in command line environment.

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
