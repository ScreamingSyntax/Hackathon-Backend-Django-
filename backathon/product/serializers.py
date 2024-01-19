from .models import *
from rest_framework.serializers import ModelSerializer

class WasteProductSerializer(ModelSerializer):
    class Meta:
        model = WasteProduct
        fields = "__all__"

class RecycledProductSerializer(ModelSerializer):
    class Meta:
        model = RecycledProduct
        fields = "__all__"

class ExchangableProductSerializer(ModelSerializer):
    class Meta:
        model = ExchangableProduct
        fields = "__all__"
