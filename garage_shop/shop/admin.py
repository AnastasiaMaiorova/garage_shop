from django.contrib import admin
from .models import *


admin.site.register(Customer)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class OilAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'artikul', 'slug', 'price', 'available', 'valume', 'stock']
    # list_filter = ['available', 'created', 'updated']


admin.site.register(Oil, OilAdmin)


class FilterAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'artikul', 'slug', 'price', 'available', 'size', 'stock']
    # list_filter = ['available', 'created', 'updated']


admin.site.register(Filter)
admin.site.register(ProductCart)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Notification)
