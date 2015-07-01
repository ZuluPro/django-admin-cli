# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BooleanModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CharModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DateModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DateTimeModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ForeignKeyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.ForeignKey(to='testapp.CharModel')),
            ],
        ),
        migrations.CreateModel(
            name='IntegerModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ManyToManyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.ManyToManyField(to='testapp.CharModel')),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field1', models.CharField(max_length=10, verbose_name=b'Field #1')),
                ('field2', models.IntegerField(verbose_name=b'Field #2')),
                ('no_verbose', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TextModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.TextField(max_length=100)),
            ],
        ),
    ]
