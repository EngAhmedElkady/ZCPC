from django.shortcuts import render
from .models import Post
from .serializers import PostApi
from rest_framework.views import APIView
from rest_framework.response import Response

# create post api for get all posts, delet post, update post
class GetAllPosts(APIView):
    def get(self , request , *args , **kwargs):
        posts = Post.objects.all()
        count = posts.count()
        serializers = PostApi(posts , many=True)
        if (count > 0):
            return Response(serializers.data)
        else:
            return Response({
                "message": "No posts"
            })
            

class GetSinglePost(APIView):
    def get(self , request , post_id , *args , **kwargs):
        try:
            post  = Post.objects.get(id=post_id)
            serializer = PostApi(post)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            })

class CreatePost(APIView):
    def get(self , request , *args ,**kwagrs):
        return Response({
            "message": "create new post"
        })
    def post(self , request , *args , **kwargs):
        try:
            serializer = PostApi(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
            else:
                return Response(serializer.errors)
            return Response(serializer.data)
        except:
            return Response({
                "message":"Error" 
            })