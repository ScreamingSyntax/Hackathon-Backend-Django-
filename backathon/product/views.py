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


class GetAllWasteProductsView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            waste_products = WasteProduct.objects.all()
            serializer = WasteProductSerializer(waste_products,many=True)
            return Response({
                "success":1,
                "message": serializer.data
            })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })
class WasteProductsView(APIView):
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
                product = WasteProduct.objects.get(id = param_value)
                # user = User.objects.get(id = product.user)
                user_serializer = UserSerializer(product.user) 
                waste_product_serializer = WasteProductSerializer(product)
                return Response({
                    "success":1,
                    "data":{
                       "product": waste_product_serializer.data,
                       "user": user_serializer.data
                    }
                })
            except WasteProduct.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The product doesn't exist"
                })
        else: 
            return Response({
                "success":0,
                "message":"Please add token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['name','description','image']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide the field {field}"
                    })
            request.data['user'] = request.user
            try:
                waste_product_serializer = WasteProductSerializer(data=request.data)
                if waste_product_serializer.is_valid():
                    waste_product_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Added Waste Product"
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
    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'id' not in request.data:
                return Response({
                    "success": 0,
                    "message": "Please provide product id"
                })
            param_value = request.data['id']
            try:
                product = WasteProduct.objects.get(id=param_value, user=request.user)
            except WasteProduct.DoesNotExist:
                return Response({
                    "success": 0,
                    "message": "The product doesn't exist"
                })

            fields_to_update = request.data
            waste_product_serializer = WasteProductSerializer(product, data=fields_to_update, partial=True)
            if waste_product_serializer.is_valid():
                waste_product_serializer.save()
                return Response({
                    "success": 1,
                    "message": "Successfully updated Waste Product"
                })
            else:
                return Response({
                    "success": 0,
                    "message": waste_product_serializer.errors
                })
        else:
            return Response({
                "success": 0,
                "message": "Please provide token"
            })
    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'id' not in request.data:
                return Response({
                    "success": 0,
                    "message": "Please provide product id"
                })
            param_value = request.data['id']
            try:
                product = WasteProduct.objects.get(id=param_value, user=request.user)
                product.delete()
            except WasteProduct.DoesNotExist:
                return Response({
                    "success": 0,
                    "message": "The product doesn't exist"
                })

            return Response({
                    "success": 1,
                    "message": "Successfully deleted Waste Product"
            })

        else:
            return Response({
                "success": 0,
                "message": "Please provide token"
            })




class GetAllRecycledProductsView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if request.user.is_authenticated:
            waste_products = RecycledProduct.objects.all()
            serializer = FetchRecycledProductSerializer(waste_products,many=True)
            return Response({
                "success":1,
                "message": serializer.data
            })
        else:
            return Response({
                "success":0,
                "message":"Please provide token"
            })

class ExchangableProductsView(APIView):
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
                product = ExchangableProduct.objects.filter(product=param_value)
                exchangeable_product_serializer = ExchangableProductSerializer(product,many=True)
                return Response({
                    "success":1,
                    "data":exchangeable_product_serializer.data
                })
            except:
                return Response({
                    "success":0,
                    "message":"Something wen't wrong"
                })  
    def post(self,request):
        if request.user.is_authenticated:
            items = ['product','item','quantity']
            for item in items:
                if item not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide {item} field"
                    })
                try:
                    print(request.data)
                    exchangable_product = ExchangableProductSerializer(data=request.data)
                    if exchangable_product.is_valid():
                        exchangable_product.save()
                        return Response({
                            "success":1,
                            "message":"Successfully added"
                        })
                    else:
                        return Response({
                            "success":0,
                            "message":exchangable_product.error_messages
                        })
                except:
                    return Response({
                        "success":0,
                        "message":"Something wen't wrong"
                    })
class RecycledProductsView(APIView):
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
                product = RecycledProduct.objects.get(id = param_value)
                recycled_product_serializer = FetchRecycledProductSerializer(product)
                return Response({
                    "success":1,
                    "data":recycled_product_serializer.data
                })
            except RecycledProduct.DoesNotExist:
                return Response({
                    "success":0,
                    "message":"The product doesn't exist"
                })
        else: 
            return Response({
                "success":0,
                "message":"Please add token"
            })
    def post(self,request):
        if request.user.is_authenticated:
            fields = ['name','description','image']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide the field {field}"
                    })
            try:
                recycled_product_serializer = RecycledProductSerializer(data=request.data)
                request.data['user'] = request.user.id
                if recycled_product_serializer.is_valid():
                    recycled_product_serializer.save()
                    return Response({
                        "success":1,
                        "message":"Successfully Added Recycled Product"
                    })
                else:
                    return Response({
                        "success":0,
                        "message":recycled_product_serializer.errors
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
    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'id' not in request.data:
                return Response({
                    "success": 0,
                    "message": "Please provide product id"
                })
            param_value = request.data['id']
            try:
                product = RecycledProduct.objects.get(id=param_value)
            except RecycledProduct.DoesNotExist:
                return Response({
                    "success": 0,
                    "message": "The product doesn't exist"
                })

            fields_to_update = request.data
            recycled_product_serializer = RecycledProductSerializer(product, data=fields_to_update, partial=True)
            if recycled_product_serializer.is_valid():
                recycled_product_serializer.save()
                return Response({
                    "success": 1,
                    "message": "Successfully updated Waste Product"
                })
            else:
                return Response({
                    "success": 0,
                    "message": recycled_product_serializer.errors
                })
        else:
            return Response({
                "success": 0,
                "message": "Please provide token"
            })
    def delete(self, request):
        if request.user.is_authenticated:
            if 'id' not in request.data:
                return Response({
                    "success": 0,
                    "message": "Please provide product id"
                })
            param_value = request.data['id']
            try:
                product = RecycledProduct.objects.get(id=param_value)
                product.delete()
            except RecycledProduct.DoesNotExist:
                return Response({
                    "success": 0,
                    "message": "The product doesn't exist"
                })

            return Response({
                    "success": 1,
                    "message": "Successfully deleted Waste Product"
            })
        else:
            return Response({
                "success": 0,
                "message": "Please provide token"
            })



