from django.db import models
from user.models import *
# Create your models here.
class Post(models.Model):
    date = models.DateTimeField(auto_now= True)
    content = models.TextField()
    media = models.FileField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
