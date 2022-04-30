from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('roundteam', views.viewsets_roundteam)
router.register('rounds', views.viewsets_round)
router.register('student', views.viewsets_student)
router.register('roundfeedback', views.viewsets_roundfeedback)

urlpatterns = [
    # 7 Viewsets
    path('rest/viewsets/', include(router.urls)),
]
