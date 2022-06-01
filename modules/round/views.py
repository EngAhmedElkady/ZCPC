from django.http import Http404
from modules.community.models import Community
from .models import Round
from .serializers import RoundSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions.community import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


# help function

# Round
class viewsets_round(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    lookup_field = 'slug'

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'create']:
            self.permission_classes = [IsAuthenticated, IsInCommunnityTeam]
        elif self.action in ['destroy']:
            self.permission_classes = [IsTeamLeader_OR_VICE]

        return [permission() for permission in self.permission_classes]

    def get_community(self, community_slug):
        community = None
        try:
            community = Community.objects.get(slug=community_slug)
            return community
        except:
            raise Http404("Community does not exist")

    def get_object(self, community_slug, slug):
        community = self.get_community(community_slug)
        queryset = Round.objects.all()
        round = get_object_or_404(queryset, community=community, slug=slug)
        self.check_object_permissions(self.request, round)
        return round

    def retrieve(self, request, community_slug, slug, *args, **kwargs):
        "retrieve the team member with community slug and username"
        instance = self.get_object(community_slug, slug)
        serializer = RoundSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, community_slug, slug, *args, **kwargs):
        instance = self.get_object(community_slug, slug)
        data = {
            "name": request.data.get('name', instance.name),
            "description": request.data.get('description', None),
            "status": request.data.get('status', instance.status)
        }
        serializer = RoundSerializer(instance=instance,
                                     data=data,
                                     partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_slug, slug, *args, **kwargs):
        instance = self.get_object(community_slug, slug)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, community_slug):
        community = self.get_community(community_slug)
        all_rounds = community.rounds.all()
        serializer = RoundSerializer(all_rounds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, community_slug):
        serializer = RoundSerializer(data=request.data)
        community = self.get_community(community_slug)
        self.check_object_permissions(self.request, community)
        serializer = RoundSerializer(
            data=request.data, context={'community': community})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)