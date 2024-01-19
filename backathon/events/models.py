from django.db import models
from user.models import User
# Create your models here.
class Events(models.Model):
    type = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField()
    location = models.TextField()
    date = models.DateTimeField(auto_now=True)
    date_of_event = models.DateTimeField()
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    