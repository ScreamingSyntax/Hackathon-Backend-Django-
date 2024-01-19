from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',UserView.as_view()),
    path('login/',UserLogin.as_view())
]
