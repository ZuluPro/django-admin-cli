from django.contrib import admin
from testapp import models


def function_does_nothing(modeladmin, request, queryset):
    pass


class TestModelAdmin(admin.ModelAdmin):
    actions = ['method_does_nothing', function_does_nothing]

    def method_without_description(self):
        return 42

    def method_with_description(self):
        return 42
    method_with_description.short_description = 'Desc FOO'

    def method_does_nothing(self, request, queryset):
        pass


admin.site.register(models.CharModel)
admin.site.register(models.IntegerModel)
admin.site.register(models.TextModel)
admin.site.register(models.BooleanModel)
admin.site.register(models.DateModel)
admin.site.register(models.DateTimeModel)
admin.site.register(models.ForeignKeyModel)
admin.site.register(models.ManyToManyModel)
admin.site.register(models.TestModel, TestModelAdmin)
