from django.urls import path
from .views import *



app_name = 'cart'


urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='cart_add'),
]


