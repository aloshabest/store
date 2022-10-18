from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'checked_out']


admin.site.register(Cart, CartAdmin)
