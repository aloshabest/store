from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', password_reset_form, name='password_reset_form'),
    path('profile/<slug:slug>/', update_profile, name='profile'),
    path('signup/', SignUp.as_view(), name='signup'),
    path(
      'logout/',
      LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),

]