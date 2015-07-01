from mock import patch
try:
    from StringIO import StringIO
except ImportError: # Py3
    from io import StringIO

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.conf import settings as se
from django.utils.timezone import now
from django.utils.dateformat import format as strftime

from admin_cli.management.commands.cli import Command
from testapp import models


class ListTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()

    def test_char(self):
        models.CharModel.objects.create(field='FOO')
        call_command('cli', 'charmodel', 'list', stdout=self.stdout)

    def test_integer(self):
        models.IntegerModel.objects.create(field=42)
        call_command('cli', 'integermodel', 'list', stdout=self.stdout)

    def test_text(self):
        models.TextModel.objects.create(field='FOO')
        call_command('cli', 'textmodel', 'list', stdout=self.stdout)

    def test_boolean(self):
        models.BooleanModel.objects.create(field=True)
        call_command('cli', 'booleanmodel', 'list', stdout=self.stdout)

    def test_date(self):
        models.DateModel.objects.create(field=now().date())
        call_command('cli', 'datemodel', 'list', stdout=self.stdout)

    def test_datetime(self):
        models.DateTimeModel.objects.create(field=now())
        call_command('cli', 'datetimemodel', 'list', stdout=self.stdout)

    def test_foreignkey(self):
        fk = models.CharModel.objects.create(field='FOO')
        models.ForeignKeyModel.objects.create(field=fk)
        call_command('cli', 'datetimemodel', 'list', stdout=self.stdout)

    def test_manytomany(self):
        m2m = models.CharModel.objects.create(field='FOO')
        ins = models.ManyToManyModel.objects.create()
        ins.field.add(m2m)
        call_command('cli', 'datetimemodel', 'list', stdout=self.stdout)


class ListFieldTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        models.TestModel.objects.create(field1='FOO', field2=42, no_verbose=6)

    def test_str(self):
        call_command('cli', 'testmodel', 'list', field=['__str__'], stdout=self.stdout)

    def test_unicode(self):
        call_command('cli', 'testmodel', 'list', field=['__unicode__'], stdout=self.stdout)

    def test_model_method(self):
        call_command('cli', 'testmodel', 'list', field=['get_double'], stdout=self.stdout)

    def test_modeladmin_method_without_description(self):
        call_command('cli', 'testmodel', 'list', field=['method_without_description'], stdout=self.stdout)

    def test_modeladmin_method_with_description(self):
        call_command('cli', 'testmodel', 'list', field=['method_with_description'], stdout=self.stdout)

    def test_undefined_field(self):
        call_command('cli', 'testmodel', 'list', field=['bad_field'], stdout=self.stdout)


class DeleteAnswerTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.obj = models.CharModel.objects.create(field='FOO')

    @patch('admin_cli.management.commands.cli.raw_input', return_value='y')
    def test_answer_yes(self, *args):
        call_command('cli', 'charmodel', 'delete', stdout=self.stdout)
        self.assertEqual(0, models.CharModel.objects.count())

    @patch('admin_cli.management.commands.cli.raw_input', return_value='n')
    def test_answer_no(self, *args):
        call_command('cli', 'charmodel', 'delete', stdout=self.stdout)
        self.assertEqual(1, models.CharModel.objects.count())

    @patch('admin_cli.management.commands.cli.raw_input', return_value='n')
    def test_answer_empty(self, *args):
        call_command('cli', 'charmodel', 'delete', stdout=self.stdout)
        self.assertEqual(1, models.CharModel.objects.count())

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_answer_all(self, *args):
        models.CharModel.objects.create(field='FOO')
        call_command('cli', 'charmodel', 'delete', stdout=self.stdout)
        self.assertEqual(0, models.CharModel.objects.count())

    @patch('admin_cli.management.commands.cli.raw_input', return_value='c')
    def test_answer_cancel(self, *args):
        models.CharModel.objects.create(field='FOO')
        call_command('cli', 'charmodel', 'delete', stdout=self.stdout)
        self.assertEqual(2, models.CharModel.objects.count())

    def test_noinput(self, *args):
        call_command('cli', 'charmodel', 'delete', noinput=True, stdout=self.stdout)
        self.assertEqual(0, models.CharModel.objects.count())


class DeleteFilterTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.obj = models.CharModel.objects.create(field='FOO')

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_dont_match(self, *args):
        call_command('cli', 'charmodel', 'delete', filter=['field=BAR'], stdout=self.stdout)
        self.assertEqual(1, models.CharModel.objects.count())

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_match(self, *args):
        call_command('cli', 'charmodel', 'delete', filter=['field=FOO'], stdout=self.stdout)
        self.assertEqual(0, models.CharModel.objects.count())


class AddTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()

    def test_char(self):
        call_command('cli', 'charmodel', 'add', field=['field=FOO'], stdout=self.stdout)
        self.assertEqual(1, models.CharModel.objects.count())

    def test_integer(self):
        call_command('cli', 'integermodel', 'add', field=['field=1'], stdout=self.stdout)
        self.assertEqual(1, models.IntegerModel.objects.count())

    def test_integer_invalid(self):
        with self.assertRaises(CommandError):
            call_command('cli', 'integermodel', 'add', field=['field=FOO'], stdout=self.stdout)
        self.assertEqual(0, models.IntegerModel.objects.count())

    def test_text(self):
        call_command('cli', 'textmodel', 'add', field=['field=FOO'], stdout=self.stdout)
        self.assertEqual(1, models.TextModel.objects.count())

    def test_boolean_false(self):
        call_command('cli', 'booleanmodel', 'add', field=['field='], stdout=self.stdout)
        self.assertEqual(1, models.BooleanModel.objects.count())
        self.assertFalse(models.BooleanModel.objects.get().field)

    def test_boolean_true(self):
        call_command('cli', 'booleanmodel', 'add', field=['field=FOO'], stdout=self.stdout)
        self.assertEqual(1, models.BooleanModel.objects.count())
        self.assertTrue(models.BooleanModel.objects.get().field)

    def test_date(self):
        date = now().date()
        field = ['field='+strftime(date, se.SHORT_DATE_FORMAT)]
        call_command('cli', 'datemodel', 'add', field=field, stdout=self.stdout)
        self.assertEqual(1, models.DateModel.objects.count())
        self.assertEqual(date, models.DateModel.objects.get().field)

    # TODO: Works but not test
    # def test_datetime(self):
    #     date = now()
    #     field = ['field='+strftime(date, se.SHORT_DATETIME_FORMAT)]
    #     field = ['field=06/30/2015-20:48']
    #     call_command('cli', 'datetimemodel', 'add', field=field, stdout=self.stdout)
    #     self.assertEqual(1, models.DateTimeModel.objects.count())
    #     self.assertEqual(date, models.DateTimeModel.objects.get().field)

    # TODO: Works but not test
    # def test_foreignkey(self):
    #     obj = models.CharModel.objects.create(field='FOO')
    #     field = ['field=%i' % obj.id]
    #     call_command('cli', 'foreignkeymodel', 'add', field=field, stdout=self.stdout)
    #     self.assertEqual(1, models.ForeignKeyModel.objects.count())

    def test_manytomany(self):
        obj = models.CharModel.objects.create(field='FOO')
        field = ['field=%i' % obj.id]
        call_command('cli', 'manytomanymodel', 'add', field=field, stdout=self.stdout)
        self.assertEqual(1, models.ManyToManyModel.objects.count())

    def test_unknow_field(self):
        with self.assertRaises(CommandError):
            call_command('cli', 'charmodel', 'add', field=['bad_field=FOO'], stdout=self.stdout)


class UpdateAnswerTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.obj = models.CharModel.objects.create(field='FOO')

    @patch('admin_cli.management.commands.cli.raw_input', return_value='y')
    def test_answer_yes(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], stdout=self.stdout)
        self.assertEqual('BAR', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='n')
    def test_answer_no(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], stdout=self.stdout)
        self.assertEqual('FOO', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='')
    def test_answer_empty(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], stdout=self.stdout)
        self.assertEqual('FOO', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_answer_all(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], stdout=self.stdout)
        self.assertEqual('BAR', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='c')
    def test_answer_cancel(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], stdout=self.stdout)
        self.assertEqual('FOO', models.CharModel.objects.get().field)

    def test_noinput(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], noinput=True, stdout=self.stdout)
        self.assertEqual('BAR', models.CharModel.objects.get().field)


class UpdateFilterTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.obj = models.CharModel.objects.create(field='FOO')

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_dont_match(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], filter=['field=BAR'], stdout=self.stdout)
        self.assertEqual('FOO', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_match(self, *args):
        call_command('cli', 'charmodel', 'update', field=['field=BAR'], filter=['field=FOO'], stdout=self.stdout)
        self.assertEqual('BAR', models.CharModel.objects.get().field)

    @patch('admin_cli.management.commands.cli.raw_input', return_value='a')
    def test_unknow_field(self, *args):
        call_command('cli', 'charmodel', 'update', field=['bad_field=BAR'], filter=['field=FOO'], stdout=self.stdout, stderr=self.stderr)
        self.assertEqual('FOO', models.CharModel.objects.get().field)


class DescribeTest(TestCase):
    def setUp(self):
        self.stdout = StringIO()

    def test_char(self):
        call_command('cli', 'charmodel', 'describe', stdout=self.stdout)

    def test_integer(self):
        call_command('cli', 'integermodel', 'describe', stdout=self.stdout)

    def test_text(self):
        call_command('cli', 'textmodel', 'describe', stdout=self.stdout)

    def test_boolean(self):
        call_command('cli', 'booleanmodel', 'describe', stdout=self.stdout)

    def test_date(self):
        call_command('cli', 'datemodel', 'describe', stdout=self.stdout)

    def test_datetime(self):
        call_command('cli', 'datetimemodel', 'describe', stdout=self.stdout)

    def test_foreignkey(self):
        call_command('cli', 'foreignkeymodel', 'describe', stdout=self.stdout)

    def test_manytomany(self):
        call_command('cli', 'manytomanymodel', 'describe', stdout=self.stdout)

    def test_testmodel(self):
        call_command('cli', 'testmodel', 'describe', stdout=self.stdout)
