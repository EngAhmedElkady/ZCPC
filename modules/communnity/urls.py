from django.urls import path, include
from .views import DisplayAllCommunity, CreateNewCommunity,DisplayCommunityTeam , DisplayAllTeams , CreateTeam , UpdateTeam , DeleteTeam , DisplaySingleTeam

urlpatterns = [
    # url for community
    path('', DisplayAllCommunity.as_view(), name="all_community"),
    path('create/', CreateNewCommunity.as_view(), name="create"),
    path("team/<int:community_id>",DisplayCommunityTeam.as_view()),
    path('', include('modules.round.urls')),
    # url for teams
    path('teams/' , DisplayAllTeams.as_view() , name="all_teams"),
    path('teams/<int:team_id>' , DisplaySingleTeam.as_view() , name="single_team"),
    path('teams/create' , CreateTeam.as_view() , name="create_team"),
    path('teams/update/<int:pk>' , UpdateTeam.as_view() , name="update_team"),
    path('teams/delete/<int:team_id>' ,DeleteTeam.as_view() , name="delete_team" ),
]
