from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', index, name='home'),
    path('shop/', shop, name='shop'),
    path('products/<slug:prod_slug>/', single, name='single'),
]
