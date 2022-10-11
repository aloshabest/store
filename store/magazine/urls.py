from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('shop/<slug:cat_slug>/', shop, name='shop'),
    path('products/<slug:prod_slug>/', Single.as_view(), name='single'),
]
