from django.shortcuts import render
from . import serializers
from . import models
from modules.level.models import Level
from rest_framework.response import Response
from permissions.community import IsInCommunnityTeam, IsTeamLeader, IsOwner
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
# help function
from permissions.helpfunction import isteamleader, incommunityteam, isinlevelteam, isinlevelstudent
from rest_condition import And, Or, Not



class viewsets_content(viewsets.ModelViewSet):
    queryset = models.Content.objects.all()
    serializer_class = serializers.ContentSerializer
    permission_classes = {
        IsInCommunnityTeam & IsAuthenticated: ['update', 'post', 'partial_update', 'destroy', 'list', 'create'],
        AllowAny & IsAuthenticated: ['retrieve']
    }

    def list(self, request, level_id):
        try:
            level = Level.objects.get(id=level_id)
            contents = level.contents.all()
            content_serializer = serializers.ContentSerializer(
                contents, many=True)
            return Response({
                "contents": content_serializer.data,
            }
            )
        except:
            return Response("level not found")

    def retrieve(self, request, pk, *args, **kwargs):
        try:
            content = models.Content.objects.get(id=pk)
            files = content.files.all()
            problems = content.problems.all()
            videos = content.videos.all()
            content_serializer = serializers.ContentSerializer(content)
            file_serializer = serializers.FileSerializer(files, many=True)
            problem_serializer = serializers.ProblemSerializer(problems, many=True)
            video_serializer = serializers.VideoSerializer(videos, many=True)
            return Response({
                "content": content_serializer.data,
                "files": file_serializer.data,
                "videos": video_serializer.data,
                "sheet": problem_serializer.data
            }
            )
        except :
            return Response({
                "contents": content_serializer.data,
                }
            )
            

    def create(self, request, level_id):
        serializer = serializers.ContentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                level = Level.objects.get(id=level_id)
                print(level)
                if incommunityteam(request.user.id, level.get_community()) == False:
                    return Response("you do not have access")
                serializer.save()
                return Response(
                    serializer.data,
                    status.HTTP_200_OK,
                )
            except:
                return Response({
                    "message": "level not found"
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            status.HTTP_400_BAD_REQUEST
        )
