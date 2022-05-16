from rest_framework import serializers
from .models import Communnity, Team

# create communnity api


class ComnunityApi(serializers.ModelSerializer):
    class Meta:
        model = Communnity
        fields = ("name",'slug',"university","owner","created_at")


class TeamApi(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["user" , 'community' , 'role' , 'start_journey' , 'end_journey' , 'status']
