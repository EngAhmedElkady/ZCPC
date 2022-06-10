from django.urls import path 
from . import views

urlpatterns = [
    path('<str:pk>/posts/' , views.GetAllPostsAndCreate.as_view()),    
    path('<str:community_name>/posts/<slug:tag_slug>' , views.GetAllPostsAndCreate.as_view()),    
    path('<str:community_name>/posts/post_detail/<slug:slug>' , views.GetSinglePostAndUpdateAndDelete.as_view()),
    # path('posts/community/<str:pk>' , views.GetCommunityPosts),
    path('<str:community_name>/posts/post_detail/<slug:post_slug>/comments/' , views.GetCommentsAndCreate.as_view()),  
    path('<str:community_name>/posts/post_detail/<slug:post_slug>/comments/<int:pk>' , views.GetCommentAndUpdateAndDelete.as_view()),
]
