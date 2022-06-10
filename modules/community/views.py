from django.http import Http404
from .models import Team
from .serializers import AddTMemeberTeam, CommunitySerializer, TeamSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from modules.community.models import Community
from rest_framework.response import Response
from permissions.community import *
from permissions.helpfunction import Community_Function
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


User = get_user_model()


class viewsets_community(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.action in ['list', 'create', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsTeamLeader_OR_VICE | IsOwner]
        elif self.action in ['destroy']:
            self.permission_classes = [IsOwner]

        return [permission() for permission in self.permission_classes]

    def get_object(self, slug):
        queryset = Community.objects.all()
        community = get_object_or_404(queryset, slug=slug)
        self.check_object_permissions(self.request, community)
        return community

    # 1 retrieve

    def retrieve(self, request, slug, *args, **kwargs):
        "return community with community slug"
        instance = self.get_object(slug)
        serializer = CommunitySerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # 2 update
    def update(self, request, slug, *args, **kwargs):
        print("update community with community slug")
        instance = self.get_object(slug)
        self.check_object_permissions(self.request, instance)

        data = {
            "name": request.data.get('name', instance.name),
            "university": request.data.get('university', instance.university),
            "bio": request.data.get('bio', instance.bio),

            # "image": request.data.get('image', instance.image),

        }
        serializer = CommunitySerializer(instance=instance,
                                         data=data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, slug, *args, **kwargs):
        instance = self.get_object(slug)
        data = {
            "name": request.data.get('name', None),
            "university": request.data.get('university', None),
            "bio": request.data.get('bio', instance.bio),

            # "image": request.data.get('image', None),

        }
        serializer = CommunitySerializer(instance=instance,
                                         data=data,
                                         partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug, *args, **kwargs):
        instance = self.get_object(slug)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        communnities = Community.objects.all()
        serializer = CommunitySerializer(communnities, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        serializer = CommunitySerializer(
            data=request.data, context={'owner': user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Team
class viewsets_team(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    model = Team
    lookup_field = 'user__username'

    # permissions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [
                IsAuthenticated, IsTeamLeader_OR_VICE | IsOwner]
       

        return [permission() for permission in self.permission_classes]
        
    # get_object

    def get_object(self, community_slug, user__username):
        queryset = Community.objects.all()
        try:
            community = get_object_or_404(queryset, slug=community_slug)
        except:
            raise Http404("Community not found")
        try:
            team = community.team.all()
            member = team.get(user__username=user__username,
                              community=community)
            self.check_object_permissions(self.request, community)
            return member
        except:
            raise Http404("member not found")

    def retrieve(self, request, community_slug, user__username, *args, **kwargs):
        "retrieve the team member with community slug and username"
        instance = self.get_object(community_slug, user__username)
        serializer = TeamSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, community_slug, user__username, *args, **kwargs):
        "update team member with community slug and username"
        instance = self.get_object(community_slug, user__username)
        data = {
            "role": request.data.get('role', instance.role),
            "status": request.data.get('status', instance.role),
        }
        serializer = TeamSerializer(instance=instance,
                                    data=data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, community_slug, user__username, *args, **kwargs):
        "update team member with community slug and username"
        instance = self.get_object(community_slug, user__username)
        data = {
            "role": request.data.get("role", instance.role),
            "status": request.data.get('status', instance.role),
        }
        serializer = TeamSerializer(instance=instance,
                                    data=data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, user__username, *args, **kwargs):
        "delete team member with community slug and username"
        try:
            community = Community.objects.get(slug=community_slug)
        except :
            raise Http404("Community not found")
        try:
            team = community.team.all()
            member = team.get(user__username=user__username)
            if Community_Function.is_in_community_team(request.user, community) or Community_Function.is_owner(request.user.username, member.user__username):
                member.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
               
        except :
            raise Http404("member not found")
            

    def list(self, request, community_slug, *args, **kwargs):
        queryset = Community.objects.all()
        community = get_object_or_404(queryset, slug=community_slug)
        team = community.team.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request, community_slug, *args, **kwargs):
        community = get_object_or_404(
            Community.objects.all(), slug=community_slug)
        self.check_object_permissions(self.request, community)
        data = {
            'email': request.data.get('email'),
            'role': request.data.get("role", 'member'),
            'status': request.data.get("status", False),
        }
        serializer = AddTMemeberTeam(
            data=data, context={'community': community})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Team member added successfully',
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
