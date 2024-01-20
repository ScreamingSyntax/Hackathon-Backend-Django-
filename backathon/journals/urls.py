from django.urls  import path
from .views import *

urlpatterns = [
    path('',JournalView.as_view())
]
