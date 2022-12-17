from django.urls import path
from .views import *

app_name = 'magazine'

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('contact/', Contact.as_view(), name='contact'),
    path('search/', Search.as_view(), name='search'),
    path('favourite/', Favourite.as_view(), name='favourite'),
    path('shop/<str:type>/<slug:cat_slug>/', Shop.as_view(), name='shop'),
    path('products/<slug:prod_slug>/', Single.as_view(), name='single'),

]
