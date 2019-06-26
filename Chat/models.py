# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Message(models.Model):
    time = models.TimeField()
    sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='messages_sender')
    receiver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='messages_receiver')
    message = models.TextField()
