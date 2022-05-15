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
    path('<slug:slug>/' , views.GetCommunityAndUpdateAndDelete.as_view()),
    #path("<slug:community_name>/team/",views.DisplayCommunityTeam.as_view()),
    path('', include('modules.round.urls')),
    # url for teams
    # path('<slug:slug>/teams/' , views.GetTeamsAndCreate.as_view()),
    path('<slug:slug>/team/<int:pk>' , views.GetTeamAndUpdateAndDelete.as_view()),
    path('<slug:slug>/team/create' , views.CreateTeam.as_view()),
    path('<slug:slug>/team/<str:username>' , views.GetTeamMemeber.as_view()),
]
