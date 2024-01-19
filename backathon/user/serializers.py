from .models import *
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name","email","password","image","phone_number","user_type"]
