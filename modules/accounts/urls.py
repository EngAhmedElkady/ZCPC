# accounts/urls.py
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


]
