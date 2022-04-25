from django.shortcuts import render
from .models import Post , Comment
from .serializers import PostApi , CommentApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status

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
    permission_classes = (IsAuthenticated,)
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


class UpdatePost(APIView):
    def put(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        serializer = PostApi(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePost(APIView):
    def delete(self , request , post_id ,  *args , **kwagrs):
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# for comments
class GetAllComment(APIView):
    def get(self , request , *args , **kwagrs):
        comments = Comment.objects.all()
        count = comments.count()
        serializers = CommentApi(comments , many=True)
        if count > 0:
            return Response(serializers.data)
        else:
            return Response({
                "message": "No Comment"
            })


class CreateComment(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self , request , *args ,**kwagrs):
        return Response({
            "message": "create new comment"
        })
    def post(self , request , *args , **kwargs):
        try:
            serializer = CommentApi(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
            else:
                return Response(serializer.errors)
            return Response(serializer.data)
        except:
            return Response({
                "message":"Error" 
            })




class DeleteComment(APIView):
    def delete(self , request , comment_id ,  *args , **kwagrs):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateComment(APIView):
    def put(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        serializer = PostApi(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
