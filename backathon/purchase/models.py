from django.db import models
from product.models import WasteProduct
from user.models import User
# Create your models here.
class WastePurchase(models.Model):
    waste_product = models.ForeignKey(WasteProduct, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_purchases_sold')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='waste_purchases_bought')
    
