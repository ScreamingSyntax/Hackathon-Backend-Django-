from rest_framework.serializers import ModelSerializer
from .models import *

class WastePurchaseSerializer(ModelSerializer):
    class Meta:
        model = WastePurchase
        fields = "__all__"

