from django.contrib import admin

from sandbox import models

admin.site.register(models.Contact)
admin.site.register(models.Restaurant)
admin.site.register(models.Sale)
admin.site.register(models.Rating)
