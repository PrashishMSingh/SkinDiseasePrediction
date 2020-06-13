# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import RestaurantBooking, HotelBooking, TravelBooking, Place, Booking

# Register your models here.
admin.site.register(Booking)
admin.site.register(RestaurantBooking)
admin.site.register(HotelBooking)
admin.site.register(TravelBooking)
admin.site.register(Place)
