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


class UserLogin(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def post(self,request):
        print(request.data)
        try:
            if "email" not in request.data:
                return Response({
                    "success":0,
                    "message": "Email is needed to login"
                },
                
                )
            if "password" not in request.data:
                return Response({
                    "success":0,
                    "message":"Password is needed to login"
                },
                )
            email = request.data['email']
            user = User.objects.get(email = email)
            if not user.check_password(request.data.get('password')):
                return Response({
                    'success': 0,
                    'message': "Wrong Password"
                },
                )
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({
                "success": 1,
                "token": token.key,
                "data": serializer.data,
                "message":"Successfully Logged In"
            })
        except BaseUser.DoesNotExist:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            },
            )
        except User.DoesNotExist:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            })
        except:
            return Response({
                "success":0,
                "message":"Customer doesn't exist"
            },
            )
class UserView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
   
    def post(self,request):
        try:
            print(request.data)
            required_fields = ["full_name","email","password","image","phone_number"]
            for fields in required_fields:
                if fields not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please input {fields} while registering up"
                    })
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                password = make_password(request.data['password'])
                user = User.objects.get(email=request.data['email'])
                user.password = password
                user.save()
                return Response({
                    "success":1,
                    "message":"Successfully Registered"
                })
            if(serializer._errors['email'][0].title() == "Base User With This Email Already Exists."):
                return Response({
                    "success":0,
                    "message":"The User already exist"
                })
            
            else:
                return Response({
                    "success":0,
                    "message":serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })

        