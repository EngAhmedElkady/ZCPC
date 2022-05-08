from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('content', views.viewsets_content)


urlpatterns = [
    path("in_level/<int:level_id>/",include(router.urls))
]
