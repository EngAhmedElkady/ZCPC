from rest_framework import serializers
from .models import Communnity, Team

# create communnity api


class ComnunityApi(serializers.ModelSerializer):
    class Meta:
        model = Communnity
        fields = ("name","university","owner","created_at")


class TeamApi(serializers.ModelSerializer):
    class Meta:
        model = Team
        exclude=("id",)
