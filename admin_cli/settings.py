from django.conf import settings

USERS = getattr(settings, 'ADMIN_CLI_USERS', {})
