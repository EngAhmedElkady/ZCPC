from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('rounds', views.viewsets_round)

urlpatterns = [

    path('rest/viewsets/', include(router.urls)),
    path("<int:community_id>/",views.CommunityRounds.as_view())
]
