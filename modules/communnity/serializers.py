from rest_framework import serializers
from .models import Communnity, Team

# create communnity api


class ComnunityApi(serializers.ModelSerializer):
    class Meta:
        model = Communnity
        fields = ("id","name","university","owner","created_at","team")


class TeamApi(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
