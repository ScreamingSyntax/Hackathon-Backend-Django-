from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('wasteProducts/',WasteProductsView.as_view()),
    path('wasteProductsAll/',GetAllWasteProductsView.as_view()),
    path('recycledProducts/',RecycledProductsView.as_view()),
    path('recycledProductsAll/',GetAllRecycledProductsView.as_view()),

]