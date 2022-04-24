from django.urls import path
from .views import GetAllPosts , GetSinglePost , CreatePost , CreateComment , GetAllComment , DeletePost , DeleteComment ,UpdateComment  , UpdatePost


urlpatterns = [
    path('posts/' , GetAllPosts.as_view() , name="all_posts"),
    path('create_post/' , CreatePost.as_view() , name="create_post"),
    path('<int:post_id>' ,GetSinglePost.as_view() , name="post"),
    path('update-post/<int:pk>' , UpdatePost.as_view() , name="update_post"),
    path('delete_post/<int:post_id>' ,DeletePost.as_view() , name="delete_post"),
    path('comments/' ,GetAllComment.as_view() , name="all_comments"),
    path('create_comment/' , CreateComment.as_view() , name="create_comment"), 
    path('delete_comment/<int:comment_id>' , DeleteComment.as_view() , name="delete_comment"),
    path('update-comment/<int:pk>' , UpdateComment.as_view() , name="update_comment"),

]