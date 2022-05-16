from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.viewsets_round)

urlpatterns = [

    path('', include(router.urls)),
    path('<slug:round_name>/', include('modules.level.urls')),

]
