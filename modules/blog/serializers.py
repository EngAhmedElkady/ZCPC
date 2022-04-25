from rest_framework import serializers
from .models import Post , Comment


class PostApi(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content' , 'title' , 'community' , 'auther']


class CommentApi(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']