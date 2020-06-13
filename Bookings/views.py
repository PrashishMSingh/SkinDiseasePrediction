# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
from datetime import datetime
from io import BytesIO

from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RestaurantBookingSerializer, HotelBookingSerializer, TravelBookingSerializer, PlaceSerializer

from Actors.models import Concierge, Tourist
from Actors.serializers import ConciergeSerializer

from .models import RestaurantBooking, HotelBooking, TravelBooking, Place, Booking


@api_view(["GET"])
def getIndex(request):
    return Response({"Result" : "Success"});

class RestaurantBookingListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        print("Printing the get request")
        tourist = Tourist.objects.get(user=request.user)
        restaurant_booking = RestaurantBooking.objects.values("no_of_people", "time", "restaurant__street").\
            filter(booking__booked_for=tourist, restaurant__type='restaurant').\
            annotate(
            booked_by=F("booking__booked_by"),
            booking_date=F("booking__date"),
            resturant=F("restaurant__name"),
            city=F("restaurant__city"),
            street=F("restaurant__street"),
        )
        print("Reached here")
        return Response(restaurant_booking, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)
        restaurant_booking_serializer = RestaurantBookingSerializer(data=data);

        if restaurant_booking_serializer.is_valid():
            restaurant_booking, error = restaurant_booking_serializer.create(data)

            if restaurant_booking:
                message = f"Sucessfully placed reservation at {data['restaurant']['name']}"
                response = {"result": "success", "message": message, "data": restaurant_booking_serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)

        error = dict(restaurant_booking_serializer.errors)
        return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)


class HotelBookingListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        tourist = Tourist.objects.get(user=request.user)

        hotel_booking = HotelBooking.objects.values("no_of_rooms", "no_of_days").\
            filter(booking__booked_for=tourist, hotel__type='hotel').\
            annotate(
            booked_by=F("booking__booked_by"),
            booking_date=F("booking__date"),
            hotel=F("hotel__name"),
            city=F("hotel__city"),
            street=F("hotel__street"),
        )
        return Response(hotel_booking, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)
        hotel_booking_serializer = HotelBookingSerializer(data=data);

        if hotel_booking_serializer.is_valid():
            hotel_booking, error = hotel_booking_serializer.create(data)

            if hotel_booking:
                message = f"Sucessfully booked {data['no_of_rooms']} " \
                    f"rooms for {data['no_of_days']} at {data['hotel']['name']}"
                response={"result": "success", "message": message, "data": hotel_booking_serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)

        error = dict(hotel_booking_serializer.errors)
        return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)


class TravelBookingListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        tourist = Tourist.objects.get(user=request.user)
        travel_booking = TravelBooking.objects.\
            values("dest_location", "initial_location", "ticket_no", "travel_mode", "travel_date").\
            filter(booking__booked_for=tourist, agency__type='travel').\
            annotate(
                booked_by=F("booking__booked_by"),
                booking_date=F("booking__date"),
                agency=F("agency__name"),
                city=F("agency__city"),
                street=F("agency__street"),
        )
        return Response(travel_booking, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)
        travel_booking_serializer = TravelBookingSerializer(data=data);

        if travel_booking_serializer.is_valid():
            travel_booking, error = travel_booking_serializer.create(data)

            if travel_booking:
                message = f"Sucessfully booked ticket {data['ticket_no']} " \
                    f" for {data['travel_mode']} at {data['travel_date']}"

                response = {"result": "success", "message": message, "data": travel_booking_serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)

        error = dict(travel_booking_serializer.errors)
        return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)


class PlaceListView(APIView):
    @staticmethod
    def get(request):
        places = Place.objects.all();
        serializer = PlaceSerializer(places, many = True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_upcoming_events(request):
    current_date =datetime.now().date()
    tourist = Tourist.objects.get(user = request.user)
    restaurants_booking = RestaurantBooking.objects.\
        filter(booking__booked_for=tourist, restaurant__type='restaurant',
               booking__date__gt=current_date).values('id').\
        annotate(
            booking_date=F("booking__date"),
            name=F("restaurant__name"),
            location=Concat(Concat(F("restaurant__city"), Value(', ')), F("restaurant__street")),
        )

    hotel_booking = HotelBooking.objects. \
        filter(booking__booked_for=tourist, hotel__type='hotel',
               booking__date__gt=current_date).values('id').\
        annotate(
            booking_date=F("booking__date"),
            name=F("hotel__name"),
            location=Concat(Concat(F("hotel__city"), Value(', ')), F("hotel__street")),
        )

    travel_booking = TravelBooking.objects. \
        filter(booking__booked_for=tourist, agency__type='travel',
               booking__date__gt=current_date).values('id').\
        annotate(
            booking_date=F("booking__date"),
            name=F("agency__name"),
            location=Concat(Concat(F("agency__city"), Value(', ')), F("agency__street")),
        )

    print("Printing the bookings")
    print(list(restaurants_booking))
    print(list(hotel_booking))
    print(list(travel_booking))

    events = itertools.chain(list(restaurants_booking), list(hotel_booking))

    upcoming_events = itertools.chain(events, list(travel_booking))
    print(upcoming_events)

    return Response({"upcoming_event" : upcoming_events})

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_past_events(request):
    current_date = datetime.now().date()
    tourist = Tourist.objects.get(user=request.user)
    restaurants_booking = RestaurantBooking.objects. \
        filter(booking__booked_for=tourist, restaurant__type='restaurant',
               booking__date__lt=current_date).values('id'). \
        annotate(
            booking_date=F("booking__date"),
            name=F("restaurant__name"),
            location=Concat(Concat(F("restaurant__city"), Value(', ')), F("restaurant__street")),
    )

    hotel_booking = HotelBooking.objects. \
        filter(booking__booked_for=tourist, hotel__type='hotel',
               booking__date__lt=current_date).values('id'). \
        annotate(
            booking_date=F("booking__date"),
            name=F("hotel__name"),
            location=Concat(Concat(F("hotel__city"), Value(', ')), F("hotel__street")),
    )

    travel_booking = TravelBooking.objects. \
        filter(booking__booked_for=tourist, agency__type='travel',
               booking__date__lt=current_date).values('id'). \
        annotate(
            booking_date=F("booking__date"),
            name=F("agency__name"),
            location=Concat(Concat(F("agency__city"), Value(', ')), F("agency__street")),
    )

    print("Printing the bookings")
    print(list(restaurants_booking))
    print(list(hotel_booking))
    print(list(travel_booking))

    events = itertools.chain(list(restaurants_booking), list(hotel_booking))

    past_events = itertools.chain(events, list(travel_booking))
    print(past_events)

    return Response({"past_event": past_events})