from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title', 'slug', 'type', 'image']
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('title',)}


class SaleAdmin(admin.ModelAdmin):
    list_display = ['prod', 'sale', 'last_price', 'new_price']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Sale, SaleAdmin)

