from django.urls import path, include
from . import views
# urlpatterns = [
#     path('', DisplayAllCommunity.as_view(), name="all_community"),
#     path('create/', CreateNewCommunity.as_view(), name="create"),
#     path("<str:community_name>/team",DisplayCommunityTeam.as_view()),
#     path("<str:community_name>/",DisplayCommunity.as_view()),
# from . import views

urlpatterns = [
    # url for community
    path('' , views.GetCommuntiesAndCreate.as_view()),
    path('community/<slug:slug>' , views.GetCommunityAndUpdateAndDelete.as_view()),
    path("team/<str:community_name>",views.DisplayCommunityTeam.as_view()),
    path('', include('modules.round.urls')),
    # url for teams
    path('teams/' , views.GetTeamsAndCreate.as_view()),
    path('teams/<int:pk>' , views.GetTeamAndUpdateAndDelete.as_view()),
]
