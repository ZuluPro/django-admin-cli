from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

___all__ = ('CharModel', 'IntegerModel', 'TextModel', 'BooleanModel'
            'DateModel', 'DateTimeModel', 'ForeignKeyModel', 'ManyToManyModel',
            'TestModel',)


class CharModel(models.Model):
    field = models.CharField(max_length=10)


class IntegerModel(models.Model):
    field = models.IntegerField()


class TextModel(models.Model):
    field = models.TextField(max_length=100)


class BooleanModel(models.Model):
    field = models.BooleanField(default=False)


class DateModel(models.Model):
    field = models.DateField()


class DateTimeModel(models.Model):
    field = models.DateTimeField()


class ForeignKeyModel(models.Model):
    field = models.ForeignKey(CharModel)


class ManyToManyModel(models.Model):
    field = models.ManyToManyField(CharModel)


@python_2_unicode_compatible
class TestModel(models.Model):
    field1 = models.CharField(max_length=10, verbose_name="Field #1")
    field2 = models.IntegerField(verbose_name="Field #2")
    no_verbose = models.IntegerField()

    def __str__(self):
        return '%s %i' % (self.field1, self.field2)
    __unicode__ = __str__

    def get_double(self):
        return self.field2 * 2
