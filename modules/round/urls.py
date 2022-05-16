from django.urls import path, include
from . import views 
from modules.communnity import views as s
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('round', views.viewsets_round)
router.register('team', s.viewsets_team)


urlpatterns = [

    path('', include(router.urls)),
    path('<slug:round_name>/', include('modules.level.urls')),

]
