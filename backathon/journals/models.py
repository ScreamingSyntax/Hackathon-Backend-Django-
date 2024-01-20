from django.db import models

# Create your models here.
class Journal(models.Model):
    title = models.CharField(max_length = 20)
    description = models.TextField()
    image = models.ImageField()
    file = models.FileField()
    type = models.CharField(max_length=10)