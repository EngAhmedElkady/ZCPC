
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('levelteam',views.viewsets_levelteam)
router.register('levels', views.viewsets_level)
# router.register('student', views.viewsets_student)
# router.register('levelfeedback', views.viewsets_levelfeedback)
# router.register('teamfeedback', views.viewsets_teamfeedback)

urlpatterns = [

    path('community/<slug:community_slug>/rounds/<slug:round_slug>/', include(router.urls)),

]
