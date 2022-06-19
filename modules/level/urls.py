
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router1 = DefaultRouter()
router2 = DefaultRouter()
router3 = DefaultRouter()
router4 = DefaultRouter()
router5 = DefaultRouter()
router1.register('levels', views.viewsets_level)
router2.register('team', views.viewsets_levelteam)
router3.register('students', views.viewsets_level_student)
router4.register('feedbacks', views.viewsets_levelfeedback)
router5.register('feedbacks', views.viewsets_levelteamfeedback)

urlpatterns = [

    path('community/<slug:community_slug>/rounds/<slug:round_slug>/',
         include(router1.urls)),
    path('community/<slug:community_slug>/rounds/<slug:round_slug>/levels/<str:name>/',
         include(router2.urls)),
    path('community/<slug:community_slug>/rounds/<slug:round_slug>/levels/<str:name>/',
         include(router3.urls)),
    path('community/<slug:community_slug>/rounds/<slug:round_slug>/levels/<str:name>/',
         include(router4.urls)),
    path('community/<slug:community_slug>/rounds/<slug:round_slug>/levels/<str:name>/team/<username>/', include(router5.urls)),

]
