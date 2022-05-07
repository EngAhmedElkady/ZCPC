from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('rounds', views.viewsets_round)

urlpatterns = [

    path('<str:community_name>/', include(router.urls)),
]
