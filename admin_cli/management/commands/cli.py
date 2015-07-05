"""
Group management commands module.
"""
import os
from datetime import datetime, date

import django
from django.core.management.base import BaseCommand, CommandError
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.dateformat import format as strftime
from django.utils import six
from django.template.defaultfilters import striptags
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from admin_cli import settings as cli_settings

REGISTRY = admin.site._registry
MODEL_NAMES = [m._meta.model_name for m in REGISTRY]
ACTIONS = ('list', 'delete', 'add', 'update', 'describe')
FACTORY = RequestFactory(user=AnonymousUser())
FALSE_REQ = FACTORY.get('')
FALSE_REQ.user = AnonymousUser()
if six.PY3:  # pragma: no cover
    unicode = str
    raw_input = input
else:  # pragma: no cover
    raw_input = raw_input


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, type=str, choices=MODEL_NAMES,
                            help="Model to manage")
        parser.add_argument('action', type=str, choices=ACTIONS,
                            help="Action to run")
        parser.add_argument('-f', '--field', type=str, action='append',
                            help="Field to add/update")
        parser.add_argument('-F', '--filter', type=str, action='append',
                            help="Field to filter in Django's lookup form, \
                            example: 'id=1' or 'name__startswith=A'")
        parser.add_argument('-o', '--order', type=str, action='append',
                            help="Field used to order, use '~' for revert \
                            example: 'name' or '~name'")
        parser.add_argument('-i', '--noinput', action='store_true',
                            help="Tells Django to NOT prompt the user for \
                            input of any kind.")

    def _get_model(self, name):
        """
        Get a registered model from its name.

        :param name: Model's name
        :type name: ``str``

        :returns: Model class
        :rtype: :class:`models.Model`

        :raises: CommandError: If model is not registered in admin
        """
        try:
            return [m for m in REGISTRY if m._meta.model_name == name][0]
        except IndexError:
            raise CommandError("Can't find model '%s' in admin registry")

    def _get_field_object(self, modeladmin, field):
        """
        Get the ``object`` defined by ``field``.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param field: Name of attribute, example ``'__str__'`` or ``'id'``
        :type field: ``str``

        :returns: :class:`admin.ModelAdmin` or :class:`models.Model`'s
                  attribute'
        """
        if hasattr(modeladmin, field):
            obj = getattr(modeladmin, field)
        elif field in modeladmin.model._meta.get_all_field_names():
            obj = modeladmin.model._meta.get_field(field)
        else:
            obj = field
        return obj

    def _get_field_width(self, modeladmin, field):
        """
        Try to define a column width from ``field`` string.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param field: Name of attribute, example ``'__str__'`` or ``'id'``
        :type field: ``str``

        :returns: Column's width
        :rtype: ``int``
        """
        field_obj = self._get_field_object(modeladmin, field)
        if isinstance(field_obj, models.CharField):
            return min(30, max(field_obj.max_length+1,
                       len(field_obj.verbose_name)))
        elif isinstance(field_obj, models.BooleanField):
            return max(6, len(self._get_field_name(modeladmin, field))+1)
        elif isinstance(field_obj, models.DateTimeField):
            return len(strftime(now(), settings.SHORT_DATETIME_FORMAT))+1
        elif isinstance(field_obj, models.DateField):
            return len(strftime(now(), settings.SHORT_DATE_FORMAT))+1
        else:
            return 21

    def _get_field_name(self, modeladmin, field):
        """
        Get a verbose name from ``field`` string.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param field: Name of attribute, example ``'__str__'`` or ``'id'``
        :type field: ``str``

        :returns: Verbose name of attribute
        :rtype: ``str``
        """
        if field in ('__str__', '__unicode__'):
            name = unicode(modeladmin.model._meta.verbose_name)
        elif field in modeladmin.model._meta.get_all_field_names():
            modelfield = modeladmin.model._meta.get_field(field)
            name = modelfield.verbose_name
        elif hasattr(modeladmin, field):
            admin_attr = getattr(modeladmin, field)
            name = admin_attr.short_description \
                if hasattr(admin_attr, 'short_description') else field
        else:
            name = field
        return name.capitalize()

    def _get_field_value(self, modeladmin, field, obj):
        """
        Get a value from ``field`` string.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param field: Name of attribute, example ``'__str__'`` or ``'id'``
        :type field: ``str``

        :param obj: Instance of model
        :type obj: :class:`models.Model`

        :returns: Value of attribute, called if callable
        :rtype: Trying ``str``
        """
        is_django16_fk = django.VERSION < (1, 7) and \
            field in obj._meta.get_all_field_names() and \
            isinstance(obj._meta.get_field(field), models.ForeignKey)
        if field.startswith('__'):
            value = getattr(obj, field)()
        # Django 1.6 doesn't support get empty FK
        elif is_django16_fk:  # pragma: no cover
            value = getattr(obj, obj._meta.get_field(field).attname)
        elif hasattr(modeladmin, field):
            value = getattr(modeladmin, field)
        elif hasattr(obj, field):
            value = getattr(obj, field)
            if isinstance(value, datetime):
                value = strftime(value, settings.SHORT_DATETIME_FORMAT)
            elif isinstance(value, date):
                value = strftime(value, settings.SHORT_DATE_FORMAT)
            elif value.__class__.__name__ == 'ManyRelatedManager':
                value = ','.join([str(a) for a in value.all()])
        else:
            value = 'N/A'
        if hasattr(value, '__call__'):
            # Some callable new instance as arg
            try:
                value = value(obj)
            except TypeError:
                value = value()
        # Remove HTML and new lines
        try:
            value = str(value).replace('\n', '')
            value = striptags(value)
        except:
            pass
        return value

    def _list(self, modeladmin, fields=[], filters={}, orders=[]):
        """
        Write instances filtered and with chosen attributes.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param fields: Fields to display, can be a :class:`admin.ModelAdmin`
                       or :class:`models.Model` attribute
        :type fields: ``dict``

        :param filters: Lookups for filters
        :type filters: ``dict``

        :param orders: Row ordering
        :type orders: ``list`` of ``str``
        """
        fields = fields or modeladmin.list_display
        field_names = [self._get_field_name(modeladmin, f) for f in fields]
        row_template = ''
        for field in fields:
            width = self._get_field_width(modeladmin, field)
            row_template += '{:%i}' % width
        self.stdout.write(row_template.format(*field_names))
        queryset = modeladmin.model.objects.filter(**filters).order_by(*orders)
        for obj in queryset:
            values = [self._get_field_value(modeladmin, field, obj)
                      for field in fields]
            row = row_template.format(*values)
            self.stdout.write(row)

    def _delete(self, modeladmin, filters={}, confirm=True):
        """
        Delete one or more instances filtered.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param filters: Lookups for filters
        :type filters: ``dict``

        :param confirm: Ask confirmation before make operation
        :type confirm: ``bool``
        """
        for obj in modeladmin.model.objects.filter(**filters):
            if confirm:
                # TODO: Declare related element
                res = raw_input("Delete '%s' ? [Yes|No|All|Cancel] " % obj)\
                    .lower()
                if not res or res.startswith('n'):
                    continue
                elif res.startswith('c'):
                    break
                elif res.startswith('a'):
                    confirm = False
            obj.delete()
            self.stdout.write("Deleted '%s'" % obj)

    def _add(self, modeladmin, fields):
        """
        Update one or more fields of all instances filtered.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param fields: Fields to defines
        :type fields: ``dict``

        :raises CommandError: If data is unvalid
        """
        instance = modeladmin.model()
        initial = dict([
            (field.name, getattr(instance, field.name))
            for field in modeladmin.model._meta.fields
        ])
        used_fields = dict([f.split('=') for f in fields])
        data = initial.copy()
        data.update(used_fields)
        for field_name, value in data.items():
            try:
                modelfield = modeladmin.model._meta.get_field(field_name)
            except models.FieldDoesNotExist:
                continue
            if isinstance(modelfield, models.ManyToManyField):
                data[field_name] = value.split(',')
        form_class = modeladmin.add_form if hasattr(modeladmin, 'add_form') \
            else modeladmin.get_form(FALSE_REQ)
        form = form_class(data=data)
        if form.is_valid():
            obj = form.save()
            self.stdout.write("Created '%s'" % obj)
        else:
            error_msg = '\n'+'\n'.join([
                ('%s: %s' % (field, err))
                for field in form.errors
                for err in form.errors[field]
            ])
            raise CommandError(error_msg)

    def _update(self, modeladmin, fields, filters={}, confirm=True):
        """
        Update one or more fields of all instances filtered.

        :param modeladmin: ModelAdmin of model
        :type modeladmin: :class:`admin.ModelAdmin`

        :param fields: Fields to update
        :type fields: ``dict``

        :param filters: Lookups for filters
        :type filters: ``dict``

        :param confirm: Ask confirmation before make operation
        :type confirm: ``bool``
        """
        for obj in modeladmin.model.objects.filter(**filters):
            if confirm:
                res = raw_input("Update '%s' ? [Yes|No|All|Cancel] " % obj)\
                    .lower()
                if not res or res.startswith('n'):
                    continue
                elif res.startswith('c'):
                    break
                elif res.startswith('a'):
                    confirm = False
            try:
                filtr = {obj._meta.pk.name: getattr(obj, obj._meta.pk.name)}
                modeladmin.model.objects.filter(**filtr).update(**fields)
                obj = modeladmin.model.objects.get(**filtr)
                self.stdout.write("Updated '%s'" % obj)
            except Exception as err:
                msg = "%s: %s" % (err.__class__.__name__, err.args[0])
                self.stderr.write(msg)

    def _describe(self, modeladmin):
        """
        Write description of a :class:`admin.ModelAdmin`, with model's fields
        and actions.

        :param modeladmin: ModelAdmin to describe
        :type modeladmin: :class:`admin.ModelAdmin`
        """
        instance = modeladmin.model()
        columns = ('Name (Verbose)', 'Type', 'Null', 'Blank', 'Choices',
                   'Default', 'Help text')
        row_template = '{:30} {:15} {:<5} {:<5} {:<20} {:<15} {:30}'
        self.stdout.write('MODEL:')
        self.stdout.write(row_template.format(*columns))
        for field in modeladmin.model._meta.fields:
            field_type = field.__class__.__name__ \
                if 'django.db.models' in field.__class__.__module__ \
                else '%s.%s' % (field.__class__.__module__,
                                field.__class__.__name__)
            self.stdout.write(row_template.format(
                ('%s (%s)' % (field.name, field.verbose_name)),
                field_type, bool(field.null), bool(field.blank),
                str(field.choices)[:20],
                self._get_field_value(modeladmin, field.name, instance),
                field.help_text))
        if modeladmin.actions:
            self.stdout.write('\n')
            self._get_actions(modeladmin)

    def _get_actions(self, modeladmin):
        """
        Write modeladmin's custom actions.

        :param modeladmin: ModelAdmin owning actions
        :type modeladmin: :class:`admin.ModelAdmin`
        """
        columns = ('Name', 'Description')
        row_template = '{!s:30} {!s:30}'
        self.stdout.write('ACTIONS:')
        self.stdout.write(row_template.format(*columns))
        for name, action_details in modeladmin.get_actions(FALSE_REQ).items():
            obj, name, verbose = action_details
            self.stdout.write(row_template.format(
                name, getattr(obj, 'short_description', '')))

    def _user_has_access(self, mode):
        """
        Checks if system user has access defined in ``django.conf.settings``.

        :param mode: ``'R'`` or ``'W'``
        :type mode: str

        :returns: True if user has access
        :rtype: ``bool``

        raises: CommandError: If user hasn't access or isn't registered
        """
        if not cli_settings.USERS:
            return True
        cur_user = os.getlogin()
        cur_uid = os.getuid()
        for key, value in cli_settings.USERS.items():
            if str(key) in (cur_user, str(cur_uid)):
                if mode.lower() in value.lower():
                    return True
                raise CommandError("User '%s' (%s) hasn't '%s' access" % (
                                   cur_user, cur_uid, mode))
        raise CommandError("User '%s' (%s) isn't registered" % (
                           cur_user, cur_uid))

    def handle(self, *args, **opts):
        model_name = opts['model'][0] if django.VERSION >= (1, 8) else args[0]
        action = opts['action'] if django.VERSION >= (1, 8) else args[1]
        fields = opts.get('field', []) or []
        filters = opts.get('filter', []) or []
        orders = [o.replace('~', '-') for o in (opts.get('order', []) or [])]
        confirm = not opts.get('noinput', False)
        model = self._get_model(model_name)
        modeladmin = REGISTRY[model]
        if action == 'list':
            self._user_has_access('R')
            filters_dict = dict([f.split('=') for f in filters])
            self._list(modeladmin, fields, filters_dict, orders)
        elif action == 'delete':
            self._user_has_access('W')
            filters_dict = dict([f.split('=') for f in filters])
            self._delete(modeladmin, filters_dict, confirm)
        elif action == 'add':
            self._user_has_access('W')
            self._add(modeladmin, fields)
        elif action == 'update':
            self._user_has_access('W')
            fields_dict = dict([f.split('=') for f in fields])
            filters_dict = dict([f.split('=') for f in filters])
            self._update(modeladmin, fields_dict, filters_dict, confirm)
        elif action == 'describe':
            self._user_has_access('R')
            self._describe(modeladmin)
