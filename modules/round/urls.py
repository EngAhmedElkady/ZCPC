from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.viewsets_round)

urlpatterns = [

    path('rounds/', include(router.urls)),
    path('rounds/<str:round_name>/', include('modules.level.urls')),

]
