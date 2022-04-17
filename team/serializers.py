from rest_framework import serializers
from .models import Team


class TeamApi(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['start_date' , 'end_date' , 'rol'] 