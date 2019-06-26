# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    gender = models.CharField(max_length= 20, choices=(("male","Male"), ("female", "Female"), ("others", "Others")))
    dob = models.DateField()
    def __str__(self):
        return self.user.email

class Concierge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    contact = models.CharField(max_length=11)
    price = models.IntegerField(default=None, null=True)
    rating = models.IntegerField()

    def __str__(self):
        return self.user.email







