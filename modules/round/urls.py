from django.apps import apps
from django.urls import path, include
from . import views
from modules.community import views as s
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
app_name = 'round'
router.register('rounds', views.viewsets_round)
urlpatterns = [

    path('community/<slug:community_slug>/', include(router.urls)),


]
