from ast import Pass
from xml.dom.pulldom import parseString
from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from .serializers import PostApi , CommentApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework import status  , generics
from permissions.blog import isAuther , isWriteComment
from taggit.models import Tag

# create post api for get all posts, delete post, update post, create post
# refactor blog code 

class GetAllPostsAndCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # get all posts
    def get(self , request , tag_slug=None ,   *args , **kwargs):
        posts = Post.objects.all()
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
        count = posts.count()
        serializers = PostApi(posts , many=True)
        if (count > 0):
            return Response(serializers.data)
        else:
            return Response({
                "message": "No posts"
            })
    # create new post
    def post(self , request , *args , **kwargs):
        try:
            serializer = PostApi(data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except:
            return Response({
                "message":"Error" 
            } , status=status.HTTP_400_BAD_REQUEST)



class GetSinglePostAndUpdateAndDelete(APIView):
    # get single post 
    permission_classes = [
        isAuther , IsAuthenticatedOrReadOnly
    ]
    def get(self , request , slug , *args , **kwargs):
        try:
            post  = Post.objects.get(slug=slug)
            serializer = PostApi(post)
            return Response(serializer.data)
        except:
            return Response({
                "message": "Error"
            } , status=status.HTTP_400_BAD_REQUEST)
    # update post  if the user is Auther
    def put(self, request, slug, format=None):
        post = Post.objects.get(slug=slug)
        serializer = PostApi(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # delete post if the user is Auther
    def delete(self , request , slug ,  *args , **kwagrs):
        post = Post.objects.get(slug=slug)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# get all posts in community 
class GetCommunityPosts(APIView):
    def get(self, request , pk,  *args , **kwargs):
        try:
            posts = Post.objects.all().filter(community=pk)
            serializer = PostApi(posts , many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "ERROR"
            } , status=status.HTTP_400_BAD_REQUEST)


# create comment api for get all comments, delete comment, update comment, create comment
# refactor comment code

class GetCommentsAndCreate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    
    
class GetCommentAndUpdateAndDelete(APIView):
    permission_classes = [isWriteComment]
    # get comment 
    def get(self, request , pk , *args , **kwargs):
        try:
            comment = Comment.objects.get(id=pk)
            serializer = CommentApi(comment)
            return Response(serializer.data)
        except:
            return Response({
                "message" : "error"
            } , status=status.HTTP_400_BAD_REQUEST)
    # delete comment 
    def delete(self , request , pk ,  *args , **kwagrs):
        comment = Comment.objects.get(id=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update comment
    def put(self, request, pk, format=None):
        comment = Comment.objects.get(id=pk)
        serializer = PostApi(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
