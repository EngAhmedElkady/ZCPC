from django.urls import path
from .views import DisplayAllCommunity , CreateNewCommunity

urlpatterns = [
    path('' , DisplayAllCommunity.as_view() , name="all_community"),
    path('create/' , CreateNewCommunity.as_view() ,name="create")
]