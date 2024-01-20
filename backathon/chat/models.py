from django.db import models
from user.models import User
# Create your models here.
class ChatBot(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE)
      question=models.CharField(max_length=5000,default='')
      answer=models.CharField(max_length=5000,default='')
      