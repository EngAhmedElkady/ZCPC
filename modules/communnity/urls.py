from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('c', views.viewsets_community)
router.register('team', views.viewsets_team)

urlpatterns = [

    path('', include(router.urls)),
    path('<slug:community_name>/round/', include('modules.round.urls')),

]
