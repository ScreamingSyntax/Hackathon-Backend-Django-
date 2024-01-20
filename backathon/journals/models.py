from django.db import models

class Journal(models.Model):
    title = models.CharField(max_length = 30)
    description = models.TextField()
    image = models.ImageField()
    file = models.FileField()
    type = models.CharField(max_length=10)