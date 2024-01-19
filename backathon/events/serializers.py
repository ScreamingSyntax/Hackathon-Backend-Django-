from rest_framework.serializers import ModelSerializer
from .models import *
from user.serializers import UserSerializer

class EventSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"

class FetchEventSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Events
        fields = "__all__"