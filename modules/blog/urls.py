from django.urls import path 
from . import views

urlpatterns = [
    path('posts/' , views.GetAllPostsAndCreate.as_view()),    
    path('posts/<slug:tag_slug>' , views.GetAllPostsAndCreate.as_view()),    
    path('posts/<slug:slug>' , views.GetSinglePostAndUpdateAndDelete.as_view()),
    path('posts/community/<str:pk>' , views.GetCommunityPosts),
    path('comments/' , views.GetCommentsAndCreate.as_view()),  
    path('comments/<int:pk>' , views.GetCommentAndUpdateAndDelete.as_view()),
]
