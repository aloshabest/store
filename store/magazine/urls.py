from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', index, name='home'),
    path('products/<slug:prod_slug>/', single, name='single'),
]
