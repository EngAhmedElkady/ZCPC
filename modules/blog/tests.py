from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post , Comment
from communnity.models import Communnity 

# test post model
class TestBlogApp(TestCase):
    def test_post_model(self):
        user = get_user_model().objects.create_user(username="abdelrahman" , email="abdo@gmail.com" , password="password")
        communnity = Communnity.objects.create(name="icpc" , university="suez canal" , owner=user)
        post = Post.objects.create(auther=user , content="body" , title="binary search" , community=communnity)
        self.assertEqual(post.auther , user)
        self.assertEqual(post.title , 'binary search')
        self.assertContains(post.title , 'body')
        self.assertContains(post.community , communnity)
    
    
    def test_comment_model(self):
        user = get_user_model().objects.create_user(username="abdelrahman" , email="abdo@gmail.com" , password="password")
        communnity = Communnity.objects.create(name="icpc" , university="suez canal" , owner=user)
        post = Post.objects.create(auther=user , content="body" , title="binary search" , community=communnity)
        comment = Comment.objects.create(post_id=post , user_id=user , content="this is awasome")
        self.assertEqual(comment.post_id , post)
        self.assertEqual(comment.user_id ,user)
        self.assertEqual(comment.content ,'This is awasome')

