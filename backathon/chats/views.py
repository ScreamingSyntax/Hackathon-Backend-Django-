from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from events.serializers import *
# from user.email import generate_otp,send_otp_email
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import *
from user.serializers import *

class GetParticularChatView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            param_value = request.query_params.get('id', None)
            if param_value == None:
                return Response({
                    "success":0,
                    "message":"Please provide product id"
                })
            try:
                user = User.objects.get(id=param_value)
                chat = NormalChat.objects.filter(reciever=user)
                chat_serializer = FetchNormalChatSerializer(chat,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "chat":
                        chat_serializer.data}
                })
            except User.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The event doesn't exist"
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })


class NormalChatView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            try:
                chat = NormalChat.objects.filter(Q(sender=request.user) | Q(reciever=request.user))
                print(chat)
                chat_serializer = FetchNormalChatSerializer(chat,many=True)
                return Response({
                    "success":1,
                    "data":chat_serializer.data
                })
            except Exception as e:
                print(e) 

                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ["reciever","message"]
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "mesage":"The field doesn't exist"
                    })
            request.data['sender'] = request.user
            try:
                chat_serializer = NormalChatSerializer(data=request.data)
                if chat_serializer.is_valid():
                    chat_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Send Chat"
                    })
                else:
                    return Response({
                        "success":0,
                        "message":chat_serializer.errors
                    })
            except Exception as e:
                print(e) 
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
class GetParticularEvetntChat(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            param_value = request.query_params.get('id', None)
            if param_value == None:
                return Response({
                    "success":0,
                    "message":"Please provide product id"
                })
            try:
                event = Events.objects.get(id=param_value)
                chat = EventChat.objects.filter(event=event)
                chat_serializer = FetchEventChat(chat,many=True)
                event_serializer = FetchEventSerializer(event)
                return Response({
                    "success":1,
                    "data":{
                        "event":event_serializer.data,
                        "chat":
                        chat_serializer.data}
                })
            except Events.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The event doesn't exist"
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })

class EventChatView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            try:
                event_chat = EventChat.objects.filter(sender=request.user)
                event_chat_serializer = FetchEventChat(event_chat,many=True)
                return Response({
                    "success":1,
                    "data":event_chat_serializer.data
                })
            except Exception as e:
                print(e) 

                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ["event","reciever","message"]
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "mesage":"The field doesn't exist"
                    })
            request.data['sender'] = request.user
            try:
                event_chat_serializer = EventChatsSerializer(data=request.data)
                if event_chat_serializer.is_valid():
                    event_chat_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Send Chat"
                    })
                else:
                    return Response({
                        "success":0,
                        "message":event_chat_serializer.errors
                    })
            except Exception as e:
                print(e) 
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })