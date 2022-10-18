from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('contact/', Contact.as_view(), name='contact'),
    path('search/', Search.as_view(), name='search'),
    path('shop/<str:type>/<slug:cat_slug>/', Shop.as_view(), name='shop'),
    path('products/<slug:prod_slug>/', product_detail, name='single'),

]
