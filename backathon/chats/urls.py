from django.urls import path
from .views import *
urlpatterns = [
    path('',NormalChatView.as_view()),
    path('user/',GetParticularChatView.as_view()),
    path('event/',EventChatView.as_view()),
    path('event/user/',GetParticularEvetntChat.as_view()),

]
