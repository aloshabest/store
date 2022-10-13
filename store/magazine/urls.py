from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('shop/<str:type>/<slug:cat_slug>/', Shop.as_view(), name='shop'),
    # path('shop/men/<slug:cat_slug>/', ShopMen.as_view(), name='shop_men'),
    # path('shop/women/<slug:cat_slug>/', ShopWomen.as_view(), name='shop_women'),
    path('products/<slug:prod_slug>/', Single.as_view(), name='single'),
]
