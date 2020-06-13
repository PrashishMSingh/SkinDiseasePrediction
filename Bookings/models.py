# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Actors.models import Tourist, Concierge
from django.db import models


class Booking(models.Model):
    date = models.DateField()
    booked_for = models.ForeignKey(Tourist, on_delete=models.SET_NULL, null=True)
    booked_by = models.ForeignKey(Concierge, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.date) + " : " + self.booked_for.user.email


class Place(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=(("hotel", "Hotel"), ("restaurant","Restaurant"), ("travel","Travel")))

    def __str__(self):
        return self.type + " - " + self.name



class RestaurantBooking(models.Model):
    time = models.TimeField()
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Place, on_delete=models.CASCADE)
    no_of_people = models.IntegerField()

    def __str__(self):
        return self.restaurant.name


class HotelBooking(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Place, on_delete=models.CASCADE)
    no_of_rooms = models.IntegerField()
    no_of_days = models.IntegerField()

    def __str__(self):
        return self.hotel.name


class TravelBooking(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    agency = models.ForeignKey(Place, on_delete=models.CASCADE)
    dest_location = models.CharField(max_length=100)
    initial_location = models.CharField(max_length=100)
    travel_mode = models.CharField(max_length=20, choices=(("airplane", "Airplane"), ("bus","Bus")))
    ticket_no = models.CharField(max_length=100);
    travel_date = models.DateField()

    def __str__(self):
        return self.agency.name








