from .views import RestaurantBookingListView, HotelBookingListView, TravelBookingListView, \
    PlaceListView, getIndex, get_upcoming_events, get_past_events
from django.urls import path

urlpatterns = [
    path('', getIndex),
    path('restaurant/', RestaurantBookingListView.as_view()),
    path('hotel/', HotelBookingListView.as_view()),
    path('travel/', TravelBookingListView.as_view()),
    path('place/', PlaceListView.as_view()),
    path('upcoming_event/', get_upcoming_events),
    path('past_event/', get_past_events)

]


