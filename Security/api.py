from django.conf.urls import url
from .views import TouristLogin
from django.urls import path

urlpatterns = [
    path('login/', TouristLogin.as_view())
]

