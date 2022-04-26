from django.urls import path
from .views import DisplayAllCommunity , CreateNewCommunity , DeleteCommunity , UpdateCommunity

urlpatterns = [
    path('' , DisplayAllCommunity.as_view() , name="all_community"),
    path('create/' , CreateNewCommunity.as_view() ,name="create") , 
    path('update-community/<int:pk>' , UpdateCommunity.as_view() ,name="update") , 
    path('delete-community/<int:community_id>' , DeleteCommunity.as_view() ,name="delete") , 
]