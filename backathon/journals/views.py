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


# Create your views here.
class JournalView(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            journal = Journal.objects.all()
            journal_serializer = JournalSerializer(journal,many=True)
            return Response({
                "success":1,
                "data":journal_serializer.data
            })
    def post(self,request):
        if request.user.is_authenticated:
            required_fields = ["title","description","image","file","type"]
            for field in required_fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"The field {field} is required"
                    })
            print(request.data)
            journal_serializer = JournalSerializer(data=request.data)
            if journal_serializer.is_valid():
                journal_serializer.save()
                return Response({
                    "success":1,
                    "message":"Successfully Added Journal"
                })
            else:
                return Response({
                    "success":0,
                    "message":journal_serializer.errors
                })