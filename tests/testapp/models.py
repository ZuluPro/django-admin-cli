from django.db import models

___all__ = ('CharModel', 'IntegerModel', 'TextModel', 'BooleanModel'
            'DateModel', 'DateTimeModel', 'ForeignKeyModel', 'ManyToManyModel'
            )


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
