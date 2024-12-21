from django.contrib import admin
from core import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.User)
admin.site.register(models.Recipe)
