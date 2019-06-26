from django.conf.urls import url
from .views import getCountries
from django.urls import path

urlpatterns = [
    path('', getCountries)
]



