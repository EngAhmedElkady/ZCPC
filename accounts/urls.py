# accounts/urls.py
<<<<<<< HEAD
from knox import views as knox_views
from .views import ChangePasswordView, RegisterAPI, LoginAPI, RetrieveUserAPIView, UpdateUserAPIView
from django.urls import path, include

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls',
         namespace='password_reset')),
    path('user-retrieve/', RetrieveUserAPIView.as_view(), name='user'),
    path('user-update/', UpdateUserAPIView.as_view(), name='user-update'),


=======
from django.urls import path, include

from .views import *

from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("signup/", SignupViewSets.as_view(), name="signup"),
    path("login/", LoginViewSets.as_view(), name="login"),

>>>>>>> origin/main
]
