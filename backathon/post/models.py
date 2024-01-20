from django.db import models
from user.models import *
# Create your models here.
class Post(models.Model):
    date = models.DateTimeField(auto_now= True)
    content = models.TextField()
    media = models.FileField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} {self.pk}"


class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete= models.CASCADE)
    text = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Post {self.post.pk}"

