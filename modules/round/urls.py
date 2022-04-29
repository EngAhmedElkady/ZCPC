from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('roundteam', views.viewsets_roundteam)
router.register('rounds', views.viewsets_round)

urlpatterns = [
     #7 Viewsets
     path('rest/viewsets/', include(router.urls)),
     ]
