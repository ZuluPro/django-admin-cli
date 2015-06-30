from django.contrib import admin
from testapp import models


admin.site.register(models.CharModel)
admin.site.register(models.IntegerModel)
admin.site.register(models.TextModel)
admin.site.register(models.BooleanModel)
admin.site.register(models.DateModel)
admin.site.register(models.DateTimeModel)
admin.site.register(models.ForeignKeyModel)
admin.site.register(models.ManyToManyModel)
