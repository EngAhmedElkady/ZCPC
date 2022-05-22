from django.urls import path, include
from . import views
from modules.communnity import views as s
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', views.viewsets_round)
# router2.register('', s.viewsets_team)


urlpatterns = [

    # path('community/<slug:community_name>/round', include(router.urls)),
    # path('community/<slug:community_name>/', include(router.url)),

    # path('<slug:round_name>/', include('modules.level.urls')),

]
