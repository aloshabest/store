from django.urls import path
from .views import *


urlpatterns = [
    path('', top_category, name='index'),
]
