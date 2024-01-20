from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# from user.email import generate_otp,send_otp_email
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *
from user.serializers import *


class ViewWasteClaims(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            waste_product = WasteProduct.objects.filter(buyer = request.user)
            waste_product_serializer = WastePurchaseSerializer(waste_product,many=True)
            return Response({
                "success":1,
                "data":waste_product_serializer.data
            })
        else:
            return Response({
                "success":0,
                "message":"Please input token"
            })
class WastePurchaseView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['waste_product']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please add the field {field}"
                    })
            request.data['buyer'] = request.user
            try:
                waste_product = WasteProduct.objects.get(id=request.data['waste_product'])
                request.data['seller'] = waste_product.user.id
            except WasteProduct.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The product doesn't exist"
                })
            waste_purchase_serializer = WastePurchaseSerializer(data=request.data)
            if waste_purchase_serializer.is_valid():
                waste_purchase_serializer.save()
                return Response({
                    "success":1,
                    "message":"Successfully Claimed"
                })
            else:
                return Response({
                    "success":0,
                    "message":waste_purchase_serializer.errors
                })
        else:
            return Response({
                "success":0,
                "message":"Please add user token"
            })