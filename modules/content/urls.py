from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router1 = DefaultRouter()
router1.register('contents', views.viewsets_content)


urlpatterns = [
    path('community/<slug:community_slug>/rounds/<slug:round_slug>/levels/<str:name>/',
         include(router1.urls)),
]
