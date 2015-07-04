=========================
Resctrict access to users
=========================

Put a ``dict`` named ``ADMIN_CLI_USERS`` in ``settings.py``. It must have
the following format:

::

  ADMIN_CLI_USERS = {
    'login': 'RW',
  }

Keys are UID or username, values are rights 'R' for read, 'W' for
write/update/delete and 'RW' for both.

By default ``ADMIN_CLI_USERS`` is ``{}`` which allows all users to make
all operations.
