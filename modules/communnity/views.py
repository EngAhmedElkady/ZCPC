from .models import Communnity, Team
from .serializers import ComnunityApi, TeamApi
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from modules.communnity.models import Communnity
from rest_framework.response import Response
from permissions.community import Community_Permission
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
# help function
User = get_user_model()

# Round


class viewsets_community(viewsets.ModelViewSet):
    queryset = Communnity.objects.all()
    serializer_class = ComnunityApi
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            community = Communnity.objects.get(slug=slug)
            serializer = ComnunityApi(community)
            return Response(serializer.data)
        except:
            return Response("Community not found")

    def update(self, request, slug, *args, **kwargs):
        try:
            community = Communnity.objects.get(slug=slug)
            if (Community_Permission.is_in_community_team(request.user, community) == False and
                    Community_Permission.is_owner(
                    request.user, community) == False
                    ):
                return Response("You don't have permission")
            serializer = ComnunityApi(community, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("community not found", status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, slug, *args, **kwargs):
        try:
            community = Communnity.objects.get(slug=slug)
            if (Community_Permission.is_in_community_team(request.user, community) == False and
                    Community_Permission.is_owner(
                    request.user, community) == False
                    ):
                return Response("You don't have permission")
            serializer = ComnunityApi(community, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("community not found", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug, *args, **kwargs):
        try:
            community = Communnity.objects.get(slug=slug)
            if (Community_Permission.is_owner(request.user, community.owner) == False):
                return Response("You don't have permission")
            community.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("community not found", status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # try:
        communnities = Communnity.objects.all()
        serializer = ComnunityApi(communnities, many=True)
        return Response(serializer.data)
        # except:
        return Response("community not found")

    def create(self, request):
        serializer = ComnunityApi(data=request.data)
        if serializer.is_valid():
            id = request.data['owner']
            if request.user.id == id:
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "you don't have access"
                )


class viewsets_team(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamApi
    lookup_field = "username"
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, community_name, username, *args, **kwargs):
        print(args, kwargs)
        try:
            community = Communnity.objects.get(slug=community_name)
        except:
            return Response("community not found")

        try:
            user = User.objects.get(username=username)
            team = community.team.get(user=user)
            serializer = TeamApi(team)
            return Response(serializer.data)
        except:
            return Response("member not found")

    def update(self, request, community_name, username, *args, **kwargs):
        try:
            team = Team.objects.get(user=User.objects.get(username=username))
            if (Community_Permission.is_teamleader_or_vise(request.user, team.get_community()) == False):
                return Response("You don't have permission")
            serializer = TeamApi(team, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("member not found", status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, community_name, username, *args, **kwargs):
        try:
            team = Team.objects.get(user=User.objects.get(username=username))
            if (Community_Permission.is_teamleader_or_vise(request.user, team.get_community()) == False):
                return Response("You don't have permission")
            serializer = TeamApi(team, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("member not found", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, community_name, username, *args, **kwargs):
        try:
            team = Team.objects.get(user=User.objects.get(username=username))
            if (Community_Permission.is_teamleader_or_vise(request.user, team.get_community()) == False):
                return Response("You don't have permission")
            team.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("member not found", status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        slug = kwargs['community_name']
        try:
            communnity = Communnity.objects.get(slug=slug)
            team = communnity.team.all()
            serializer = TeamApi(team, many=True)
            return Response(serializer.data)
        except:
            return Response("community not found")

    def create(self, request, *args, **kwargs):
        serializer = TeamApi(data=request.data)
        community_id = request.data['community']
        ans = True
        communnity = Communnity.objects.get(id=community_id)
        team = communnity.team.all()
        try:
            user = team.get(user=User.objects.get(id=request.data['user']))
            ans = False
        except:
            ans = True
        if serializer.is_valid() and ans:
            if (Community_Permission.is_teamleader_or_vise(request.user, communnity) or
                    Community_Permission.is_owner(request.user, communnity)
                ):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response("You don't have permission")

        return Response(
            "may be user have a position"
        )
