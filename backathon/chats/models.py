from django.db import models
from events.models import *
from user.models import User
# Create your models here.
class EventChat(models.Model):
    event = models.ForeignKey(Events,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='event_sender_chat')
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name='event_reciever_chat')
    message = models.TextField()

class NormalChat(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_chat')
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever_chat')
    message = models.TextField()
