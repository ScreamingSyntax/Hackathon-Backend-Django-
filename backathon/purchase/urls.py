from django.urls import path
from .views import *
urlpatterns = [
    path('waste/',WastePurchaseView.as_view()),
    path('waste/claims/',ViewWasteClaims.as_view()),


]
