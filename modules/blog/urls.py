from django.urls import path 
from . import views

urlpatterns = [
    path('posts/' , views.GetAllPostsAndCreate.as_view()),    
    path('posts/<int:pk>' , views.GetSinglePostAndUpdateAndDelete.as_view()),
    path('posts/community/<int:pk>' , views.GetCommunityPosts),
    path('comments/' , views.GetCommentsAndCreate.as_view()),  
    path('comments/<int:pk>' , views.GetCommentAndUpdateAndDelete.as_view()),
]
