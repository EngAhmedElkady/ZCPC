from .models import Communnity, Team
from .serializers import ComnunityApi,TeamApi
from rest_framework.views import APIView
from rest_framework.response import Response


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

