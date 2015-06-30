"""
Group management commands module.
"""
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

REGISTRY = admin.site._registry
MODEL_NAMES = [m._meta.model_name for m in REGISTRY]
ACTIONS = ('list', 'delete', 'add', 'update', 'describe')
FACTORY = RequestFactory(user=AnonymousUser())
FALSE_REQ = FACTORY.get('')
unicode = str if six.PY3 else unicode


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, type=str, choices=MODEL_NAMES)
        parser.add_argument('action', type=str, choices=ACTIONS)
        # Can't use below with Django < 1.8
        parser.add_argument('-f', '--field', type=str, action='append')
        parser.add_argument('-F', '--filter', type=str, action='append')
        parser.add_argument('-i', '--noinput', action='store_true')

    def _get_model(self, name):
        return [m for m in REGISTRY if m._meta.model_name == name][0]

    def _get_field_object(self, modeladmin, field):
        if hasattr(modeladmin, field):
            obj = getattr(modeladmin, field)
        elif field in modeladmin.model._meta.get_all_field_names():
            obj = modeladmin.model._meta.get_field(field)
        else:
            obj = field
        return obj

    def _get_field_width(self, modeladmin, field):
        field_obj = self._get_field_object(modeladmin, field)
        if isinstance(field_obj, models.CharField):
            return min(30, max(field_obj.max_length+1, len(field_obj.verbose_name)))
        elif isinstance(field_obj, models.BooleanField):
            return max(6, len(self._get_field_name(modeladmin, field))+1)
        elif isinstance(field_obj, models.DateTimeField):
            return len(strftime(now(), settings.SHORT_DATETIME_FORMAT))+1
        elif isinstance(field_obj, models.DateField):
            return len(strftime(now(), settings.SHORT_DATE_FORMAT))+1
        else:
            return 21

    def _get_field_name(self, modeladmin, field):
        if field in ('__str__', '__unicode__'):
            name = unicode(modeladmin.model._meta.verbose_name)
        elif field in modeladmin.model._meta.get_all_field_names():
            modelfield = modeladmin.model._meta.get_field(field)
            name = modelfield.verbose_name
        elif hasattr(modeladmin, field):
            admin_attr = getattr(modeladmin, field)
            if hasattr(admin_attr, 'short_description'):
                name = admin_attr.short_description
        else:
            name = field
        return name.capitalize()

    def _get_field_value(self, modeladmin, field, obj):
        if field.startswith('__'):
            value = getattr(obj, field)()
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
            value = value(obj)
        try:
            value = str(value).replace('\n', '')
            value = striptags(value)
        except:
            pass
        return value

    def _list(self, modeladmin, fields=[], filters={}):
        fields = fields or modeladmin.list_display
        field_names = [self._get_field_name(modeladmin, f) for f in fields]
        row_template = ''
        for field in fields:
            width = self._get_field_width(modeladmin, field)
            row_template += '{:%i}' % width
        self.stdout.write(row_template.format(*field_names))
        for obj in modeladmin.model.objects.filter(**filters):
            values = [self._get_field_value(modeladmin, field, obj)
                      for field in fields]
            row = row_template.format(*values)
            self.stdout.write(row)

    def _delete(self, modeladmin, filters={}, confirm=True):
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
        form = modeladmin.get_form(FALSE_REQ)(data=data)
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
                self.stderr.write("%s: %s" % (err.__class__.__name__, err.args[0]))

    def _describe(self, modeladmin):
        columns = ('Name (Verbose)', 'Type', 'Null', 'Blank', 'Choices', 'Default', 'Help text')
        row_template = '{:30} {:15} {:<5} {:<5} {:<20} {:<15} {:30}'
        self.stdout.write('MODEL:')
        self.stdout.write(row_template.format(*columns))
        for field in modeladmin.model._meta.fields:
            self.stdout.write(row_template.format(
                ('%s (%s)' % (field.name, field.verbose_name)),
                field.__class__.__name__ if 'django.db.models' in field.__class__.__module__ else '%s.%s' % (field.__class__.__module__, field.__class__.__name__),
                bool(field.null), bool(field.blank),
                str(field.choices)[:20],
                self._get_field_value(modeladmin, field.name, modeladmin.model()),
                field.help_text))
        if modeladmin.actions:
            self.stdout.write('\n')
            self._get_actions(modeladmin)

    def _get_actions(self, modeladmin):
        columns = ('Name', 'Description')
        row_template = '{:30} {:30}'
        self.stdout.write('ACTIONS:')
        self.stdout.write(row_template.format(*columns))
        for action in modeladmin.actions:
            self.stdout.write(row_template.format(
                action, getattr(modeladmin, action).short_description))

    def handle(self, *args, **opts):
        model_name = opts['model'][0] if django.VERSION >= (1, 8) else args[0]
        action = opts['action'] if django.VERSION >= (1, 8) else args[1]
        fields = opts.get('field', []) or []
        filters = opts.get('filter', []) or []
        confirm = not opts.get('noinput', False)
        model = self._get_model(model_name)
        modeladmin = REGISTRY[model]
        if action == 'list':
            filters_dict = dict([f.split('=') for f in filters])
            self._list(modeladmin, fields, filters_dict)
        elif action == 'delete':
            filters_dict = dict([f.split('=') for f in filters])
            self._delete(modeladmin, filters_dict, confirm)
        elif action == 'add':
            self._add(modeladmin, fields)
        elif action == 'update':
            fields_dict = dict([f.split('=') for f in fields])
            filters_dict = dict([f.split('=') for f in filters])
            self._list(modeladmin, fields, filters_dict)
            self._update(modeladmin, fields_dict, filters_dict, confirm)
        elif action == 'describe':
            self._describe(modeladmin)
