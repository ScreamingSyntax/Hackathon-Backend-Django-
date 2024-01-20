from .models import *
from rest_framework.serializers import ModelSerializer
class ChatSerializer(ModelSerializer):
    class Meta:
        model = ChatBot
        fields = "__all__"