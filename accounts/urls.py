# accounts/urls.py
from django.urls import path, include

from .views import *

from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("signup/", SignupViewSets.as_view(), name="signup"),
    path("login/", LoginViewSets.as_view(), name="login"),

]
