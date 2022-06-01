from django.http import Http404
from .models import Level, LevelFeedback, LevelTeam, Student, TeamFeedback
from .serializers import *
from modules.community.models import Community
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions.community import *
from django.shortcuts import get_object_or_404


# level
class viewsets_level(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    lookup_field = 'name'

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'create']:
            self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
        elif self.action == 'destroy':
            self.permission_classes = [IsTeamLeader_OR_VICE]

        return [permission() for permission in self.permission_classes]

    def get_community(self, community_slug):
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community not found")

    def get_object(self, community_slug, round_slug, name):
        community_ = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(
            queryset, community=community_, slug=round_slug)
        levels = round.levels.all()
        level = get_object_or_404(levels, name=name)
        self.check_object_permissions(self.request, community_)
        return level

    def list(self, request, community_slug, round_slug):
        community = self.get_community(community_slug)
        rounds = community.rounds.all()
        round = get_object_or_404(
            rounds, community=community, slug=round_slug)
        levels = round.levels.all()
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug, round_slug, name)
        serializer = LevelSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request,community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug,round_slug,name)
        data = {
            "name": request.data.get('name', instance.name),
            "description": request.data.get('description', None),
            "status": request.data.get('status', instance.status)
        }
        serializer = LevelSerializer(instance=instance,
                                     data=data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, round_slug, name, *args, **kwargs):
        instance = self.get_object(community_slug, round_slug, name)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, community_slug, round_slug):
        
        community = self.get_community(community_slug)
        rounds = community.rounds.all()
        round = get_object_or_404(
            rounds, community=community, slug=round_slug)
        self.check_object_permissions(self.request, community)
        serializer = LevelSerializer(
            data=request.data, context={'round': round})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class viewsets_levelteam(viewsets.ModelViewSet):
#     queryset = LevelTeam.objects.all()
#     serializer_class = LevelTeamSerializer

#     def get_permissions(self):

#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [IsAuthenticated]
#         elif self.action in ['update', 'partial_update', 'create']:
#             self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
#         elif self.action in ['destroy']:
#             self.permission_classes = [IsTeamLeader_OR_VICE]

#         return [permission() for permission in self.permission_classes]

#     def get_community(self, community_slug):
#         community = None
#         try:
#             community = Community.objects.get(slug=community_slug)
#             return community
#         except:
#             return Response("community not found")

#     def get_object(self, community_slug, round_slug, name):
#         community = self.get_community(community_slug)
#         queryset = Round.objects.all()
#         round = get_object_or_404(
#             queryset, community=community, slug=round_slug)
#         levels = round.levels.all()
#         level = get_object_or_404(levels, name=name)
#         self.check_object_permissions(self.request, community)
#         return level

#     def create(self, request):
#         serializer = LevelTeamSerializer(data=request.data)
#         if serializer.is_valid():
#             level_id = request.data['level']
#             level = Level.objects.get(id=level_id)
#             community_id = level.get_community()
#             if isteamleader(request.user.id, community_id):
#                 serializer.save()
#                 return Response(
#                     serializer.data,
#                     status=status.HTTP_201_CREATED
#                 )
#             else:
#                 return Response(
#                     "you don't have access"
#                 )
#         return Response(
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class viewsets_student(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     def create(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             level_id = request.data['level']
#             level = Level.objects.get(id=level_id)
#             if(level.status == False):
#                 return Response("The Round Closed")
#             if(request.data['user'] != str(request.user.id)):
#                 print(type(request.data['user']), type(request.user.id))
#                 print('1' == 1)
#                 return Response("make sure you are user")

#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status.HTTP_200_OK,
#             )


# class viewsets_levelfeedback(viewsets.ModelViewSet):
#     queryset = LevelFeedback.objects.all()
#     serializer_class = LevelFeedbackSerializer

#     def create(self, request):
#         serializer = LevelFeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             level_id = request.data['level']
#             if isinlevelstudent(request.data['user'], level_id) == False or str(request.user.id) != request.data['user']:
#                 return Response("sure you in this round")

#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status.HTTP_200_OK,
#             )

#         return Response(
#             status.HTTP_400_BAD_REQUEST
#         )


# class viewsets_teamfeedback(viewsets.ModelViewSet):
#     queryset = TeamFeedback.objects.all()
#     serializer_class = TeamFeedbackSerializer

#     def create(self, request):
#         serializer = TeamFeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             level_id = request.data['level']
#             if request.user.id != int(request.data['user']) or isinlevelstudent(request.user.id, level_id) == False or isinlevelteam(request.data['team_member'], level_id) == False:
#                 return Response("sure you in this round")

#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status.HTTP_200_OK,
#             )

#         return Response(
#             status.HTTP_400_BAD_REQUEST
#         )
