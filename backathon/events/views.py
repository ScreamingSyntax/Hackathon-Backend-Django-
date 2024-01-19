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

class EventsView(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            event = Events.objects.all()
            event_serializer = FetchEventSerializer(event,many=True)
            return Response({
                "success":1,
                "data":event_serializer.data
            })
        else:
            return Response({
                "success":0,
                "message":"Please Add token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['type','description','image','location','date_of_event']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please add field {field}"
                    })
            print(request.data)
            request.data['user'] = request.user
            print(request.data)
            event_serializer = EventSerializer(data=request.data)
            if event_serializer.is_valid():
                event_serializer.save()
                return Response({
                    "success":1,
                    "message":"Event Successfully Added"
                })
            else:
                return Response({
                    "success":0,
                    "message":event_serializer.errors
                })