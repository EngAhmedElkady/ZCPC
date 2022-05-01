from django.urls import path, include
from .views import DisplayAllCommunity, CreateNewCommunity,DisplayCommunityTeam

urlpatterns = [
    path('', DisplayAllCommunity.as_view(), name="all_community"),
    path('create/', CreateNewCommunity.as_view(), name="create"),
    path("team/<int:community_id>",DisplayCommunityTeam.as_view()),
]
