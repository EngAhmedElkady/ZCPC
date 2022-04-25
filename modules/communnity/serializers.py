from rest_framework import serializers
from .models import Communnity

# create communnity api 
class ComnunityApi(serializers.ModelSerializer):
    class Meta:
        model = Communnity
        fields = '__all__'