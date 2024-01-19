from django.urls import path
from .views import *
urlpatterns = [
    path('',EventsView.as_view())
]
