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


class CommentsView(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            param_value = request.query_params.get('id', None)
            print(param_value)
            if param_value == None:
                return Response({
                    "success":0,
                    "message":"Please provide product id"
                })
            print(type(int(param_value)))
            id = int(param_value)
            print(request.data)
            try:
                post = Post.objects.get(id=id)
                comment = Comments.objects.filter(post=post)
                comment_serializer = FetchCommentSerializer(comment,many=True)
                return Response({
                       "success":1,
                       "data":comment_serializer.data
                   })
            except Post.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The post doesn't exist"
                })
            # try:
            #     post = Post.objects.get(id= str(id))
            #     comment = Comments.objects.filter(post=post)
            #     comment_serializer = CommentSerializer(comment,many=True)
            #     return Response({
            #         "success":1,
            #         "data":comment_serializer.data
            #     })

        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })     
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['post','text']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please add the field {field}"
                    })
            data = dict(request.data)
            data['user']=request.user.id
            print(request.data)
            post_serializer = CommentSerializer(data=data)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response({
                    "success":1,
                    "message":"Successfully added Post"
                })
            else:
                print(post_serializer.errors)
                return Response({
                    "success":0,
                    "message":post_serializer.error_messages
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            }) 
class PostView(APIView):
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            post = Post.objects.all()
            post_serializer = FetchPostSerializer(post,many=True)
            return Response({
                "success":1,
                "data":post_serializer.data
            })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })
    def delete(self,request):
        if request.user.is_authenticated:
            try:
                if 'id' not in request.data:
                    return Response({
                        "success":0,
                        "message":"Please enter id of the post"
                    })
                id = request.data['id']
                post = Post.objects.get(id=id)
                post.delete()                
            except Post.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The post doesn't exist"
                })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['content','media','user']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide the field {field}"
                    })
            request.data['user'] = request.user
            try:
                waste_product_serializer = PostSerializer(data=request.data)
                if waste_product_serializer.is_valid():
                    waste_product_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Added Post"
                    })
                else:
                    return Response({
                        "success":0,
                        "message":waste_product_serializer.errors
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