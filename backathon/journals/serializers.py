from rest_framework.serializers import ModelSerializer
from .models import *

class JournalSerializer(ModelSerializer):
    class Meta:
        model = Journal
        fields = "__all__"