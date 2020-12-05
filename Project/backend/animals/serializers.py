from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import *


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'

class AnimalImageSerializer(serializers.ModelSerializer):
    upload_user = UserSerializer(required=False)
    class Meta:
        model = AnimalImage
        fields = ['upload_image', 'upload_date', 'animal', 'upload_user']
