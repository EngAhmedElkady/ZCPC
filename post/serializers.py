from rest_framework import serializers
from .models import Post


class PostApi(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content' , 'title' , 'community' , 'auther']