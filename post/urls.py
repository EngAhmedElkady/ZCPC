from django.urls import path
from .views import GetAllPosts , GetSinglePost , CreatePost


urlpatterns = [
    path('' , GetAllPosts.as_view() , name="all_posts"),
    path('create/' , CreatePost.as_view() , name="create"),
    path('<int:post_id>' ,GetSinglePost.as_view() , name="post"),
]