from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router2 = DefaultRouter()

router.register('', views.viewsets_community)
router2.register('', views.viewsets_team)

urlpatterns = [

    path('community/', include(router.urls)),
    path('community/<slug:community_slug>/team/',
         include(router2.urls)),


]
