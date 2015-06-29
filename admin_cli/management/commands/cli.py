"""
Group management commands module.
"""
from datetime import datetime, date

from django.core.management.base import BaseCommand, CommandError
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.dateformat import format as strftime

from optparse import make_option
from os import devnull
import sys

REGISTRY = admin.site._registry
MODEL_NAMES = [m._meta.model_name for m in REGISTRY]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('model', nargs=1, type=str, required=True,
                            choices=MODEL_NAMES)
        parser.add_argument('action', type=str, required=True)

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
            return min(20, max(field_obj.max_length+1, len(field_obj.verbose_name)))
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
        else:
            value = '?'
        if hasattr(value, '__call__'):
            value = value(obj)
        try:
            value = str(value).replace('\n', '')
        except:
            pass
        return value

    def _list(self, modeladmin):
        fields = modeladmin.list_display
        field_names = [self._get_field_name(modeladmin, f) for f in fields]
        row_template = ''
        for field in fields:
            width = self._get_field_width(modeladmin, field)
            row_template += '{:%i}' % width
        self.stdout.write(row_template.format(*field_names))
        for obj in modeladmin.model.objects.all():
            values = [self._get_field_value(modeladmin, field, obj)
                      for field in fields]
            row = row_template.format(*values)
            self.stdout.write(row)

    def handle(self, *args, **opts):
        model_name = args[0]
        action = args[1]
        model = self._get_model(model_name)
        modeladmin = REGISTRY[model]
        self._list(modeladmin)
