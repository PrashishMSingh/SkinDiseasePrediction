from django.conf.urls import url
from .views import index, TouristListView, ConciergeListView, ConciergeDetailView
from django.urls import path

urlpatterns = [
    path('', index),
    path('register/tourist/', TouristListView.as_view()),
    path('register/concierge/', ConciergeListView.as_view()),
    path('register/concierge/<int:concierge_id>/', ConciergeDetailView.as_view())
]


