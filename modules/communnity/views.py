from sys import api_version
from django.shortcuts import render
from .models import Communnity
from .serializers import ComnunityApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

# display all coummunity
class DisplayAllCommunity(APIView):
    def get(self , request , *args , **kwargs):
        communites = Communnity.objects.all()
        count = Communnity.objects.all().count()
        serializer = ComnunityApi(communites , many=True)
        if (count > 0):
            return Response(serializer.data)
        else:
            return Response({
                "message": "No community"
            })


class CreateNewCommunity(APIView):
    def get(self , request , *args , **kwargs):
        return Response({
            "message": "create new community"
        })
    def post(self , request , *args , **kwargs):
        serializer = ComnunityApi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)




class UpdateCommunity(APIView):
    def put(self, request, pk, format=None):
        community = Communnity.objects.get(id=pk)
        serializer = ComnunityApi(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommunity(APIView):
    def delete(self , request , community_id ,  *args , **kwagrs):
        community = Communnity.objects.get(id=community_id)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
