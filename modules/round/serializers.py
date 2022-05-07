from rest_framework import serializers
from .models import Round
# create round api


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'
        
