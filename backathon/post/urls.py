from django.urls import path,include
from .views import *
urlpatterns = [
    path('',PostView.as_view()),
    path('comment/',CommentsView.as_view()),

]