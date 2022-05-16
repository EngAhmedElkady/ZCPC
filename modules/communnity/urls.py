from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.viewsets_community)

urlpatterns = [

    path('', include(router.urls)),
    path('<slug:community_name>/', include('modules.round.urls')),

]
