from django.urls import path, include
from . import views

urlpatterns = [
    # url for community
    path('' , views.GetCommuntiesAndCreate.as_view()),
    path('community/<int:pk>' , views.GetCommunityAndUpdateAndDelete.as_view()),
    path("team/<int:community_id>",views.DisplayCommunityTeam.as_view()),
    path('', include('modules.round.urls')),
    # url for teams
    path('teams/' , views.GetTeamsAndCreate.as_view()),
    path('teams/<int:pk>' , views.GetTeamAndUpdateAndDelete.as_view()),
]
