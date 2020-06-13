# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tourist, Concierge

# Register your models here.
admin.site.register(Tourist)
admin.site.register(Concierge)

