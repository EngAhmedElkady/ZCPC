from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.viewsets_community)
router.register('', views.viewsets_team)

urlpatterns = [

    path('', include(router.urls)),
    path('team/', include(router.urls)),

]
