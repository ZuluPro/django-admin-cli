=======
Actions
=======

As a Django command, Admin CLI is launched by ::

  ./manage.py cli <model_name> <action>

All CRUD actions are available Create/List/Update/Delete. All filters
are based on `Django's QuerySet`_, so List/Update/Delete has ``--filter``
(``-F``) argument for act as in `Django's Lookups`_.

Add and filter actions use a ``Form`` issued from ``ModelForm.get_form`` to
get default values, valid submitted data and return errors to user.

List
====

By default Admin CLI print the fields defined in ``ModelAdmin.list_display``,
in facts it is able to print:

- A field of model
- A callable that accepts one parameter for the model instance
- An attribute on the ``ModelAdmin``
- An attribute on the model

You can specify which fields/attributes you want with ``'--field'``
(``'-f'``).

List model's instance
---------------------

A basic listing is made as below: ::

  $ ./manage.py cli user list
  Username                      Email address                 First name                    Last name                     Staff status
  zulu                                                                                                                    True
  admin                                                                                                                   True
    
List specified fields
---------------------

You can choose which field(s) you want to display with ``'--field'``
(``'-f'``): ::

  $ ./manage.py cli user list -f id -f username
  Id                   Username
  1                    zulu
  2                    admin

Filter specified fields
-----------------------

With Django's QuerySet syntax ``'--filter'`` (``'-F'``): ::

  $ ./manage.py cli user list -F id=1
  Username                      Email address                 First name                    Last name                     Staff status
  zulu                                                                                                                    True

Order by
--------

And of course ordering with ``'--order'`` (``'-o``): ::

  $ ./manage.py cli user list -f username -o username
  Username
  admin
  zulu

The reverse ordering is made by prefixing field's name by ``'~'``, (instead
of ``'-'`` like in Django): ::

  $ ./manage.py cli user list -f username -o ~username
  Username
  zulu
  admin

Add
===

Every field must be set with ``'--field'`` (``'-f'``). ``ForeignKey`` is
defined by their primary key's value. Same for ``ManyToManyField`` except
it's defined by with ``','`` as separator.

Add an instance
---------------

Create an instance with ``domain`` and ``name`` as ``CharField``: ::

  $ ./manage.py cli site add -f domain=mysite.org -f 'name=My site'
  Created 'mysite.org'

Update
======

Updates are made one by one, on every instances matching with given filters
(``'--filter'``). It updates only field specified by ``'--field'``.


Update an instance
------------------

Update an instance found from its ``domain``: ::

  $ ./manage.py cli site update -F domain=mysite.org -f 'name=New name'
  Update 'mysite.org' ? [Yes|No|All|Cancel] y
  Updated 'mysite.org'

Delete
======

Delete every instance matching with given filters (``'--filter'``).

Delete an instance
------------------

Delete an instance found from its ``domain``: ::

  $ ./manage.py cli site delete -F domain=mysite.org
  Delete 'mysite.org' ? [Yes|No|All|Cancel] y
  Deleted 'mysite.org'

Describe
========

Display ``Model``'s field and ``ModelAdmin.action``: ::

  $ ./manage.py cli site describe
  MODEL:
  Name (Verbose)                 Type            Null  Blank Choices              Default         Help text
  id (ID)                        AutoField       0     1     []                   None
  domain (domain name)           CharField       0     0     []
  name (display name)            CharField       0     0     []


.. _`Django's Lookups`: https://docs.djangoproject.com/en/1.8/topics/db/queries/
.. _`Django's QuerySet`: https://docs.djangoproject.com/en/1.8/ref/models/querysets/
