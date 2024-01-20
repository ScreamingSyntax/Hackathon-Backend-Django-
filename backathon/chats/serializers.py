from rest_framework.serializers import ModelSerializer
from .models import *
from user.serializers import *

class EventChatsSerializer(ModelSerializer):
    class Meta:
        model = EventChat
        fields = "__all__"

class FetchEventChat(ModelSerializer):
    # sender = UserSerializer()
    reciever = UserSerializer()
    class Meta:
        model = EventChat
        fields = "__all__"



class NormalChatSerializer(ModelSerializer):
    class Meta:
        model = NormalChat
        fields = "__all__"

class FetchNormalChatSerializer(ModelSerializer):
    reciever = UserSerializer()
    class Meta:
        model = NormalChat
        fields = "__all__"