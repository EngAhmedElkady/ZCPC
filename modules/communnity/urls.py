from django.urls import path, include
from .views import DisplayAllCommunity, CreateNewCommunity,DisplayCommunityTeam,DisplayCommunity

urlpatterns = [
    path('', DisplayAllCommunity.as_view(), name="all_community"),
    path('create/', CreateNewCommunity.as_view(), name="create"),
    path("<str:community_name>/team",DisplayCommunityTeam.as_view()),
    path("<str:community_name>/",DisplayCommunity.as_view()),
]
