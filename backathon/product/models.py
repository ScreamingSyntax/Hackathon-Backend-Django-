from django.db import models
from user.models import User
# Create your models here.
class WasteProduct(models.Model):
    name = models.CharField(max_length = 20)
    description = models.TextField()
    image = models.ImageField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class RecycledProduct(models.Model):
    name = models.CharField(max_length = 20)
    description = models.TextField()
    image = models.ImageField()

class ExchangableProduct(models.Model):
    product = models.ForeignKey(RecycledProduct,on_delete = models.CASCADE)
    item = models.CharField(max_length = 20)
    quantity = models.IntegerField()