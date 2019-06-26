from .models import Booking, HotelBooking, RestaurantBooking, TravelBooking, Place
from rest_framework import serializers
from Actors.models import Tourist, Concierge


class BookingSerializer(serializers.ModelSerializer):
    booked_for = serializers.PrimaryKeyRelatedField(queryset=Tourist.objects.all())
    booked_by = serializers.PrimaryKeyRelatedField(queryset=Tourist.objects.all())

    class Meta:
        model = Booking
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"


class RestaurantBookingSerializer(serializers.Serializer):
    booking = BookingSerializer()
    restaurant = PlaceSerializer()

    def create(self, validated_data):
        booking_data = validated_data.pop('booking')
        booking = Booking.objects.create(**booking_data)
        booking.save()

        validated_data["booking"] = booking
        restaurant_booking = RestaurantBooking.objects.create(**validated_data)

        restaurant_booking.save()
        return restaurant_booking

    def update(self, instance, validated_data):
        instance.restaurant = validated_data.get('resturant')
        instance.no_of_people = validated_data.get('no_of_people')
        instance.time = validated_data.get('time')


class HotelBookingSerializer(serializers.Serializer):
    booking = BookingSerializer()
    hotel = PlaceSerializer;

    def create(self, validated_data):
        booking_data = validated_data.pop('booking')
        booking = Booking.objects.create(**booking_data)
        booking.save()

        validated_data["booking"] = booking
        hotel_booking = HotelBooking.objects.create(**validated_data)
        hotel_booking.save()
        return hotel_booking

    def update(self, instance, validated_data):
        instance.hotel = validated_data.get('hotel')
        instance.no_of_rooms = validated_data.get('no_of_rooms')
        instance.save()


class TravelBookingSerializer(serializers.Serializer):
    booking = BookingSerializer()
    agency = PlaceSerializer()

    def create(self, validated_data):
        booking_data = validated_data.pop('booking')
        booking = Booking.objects.create(**booking_data)
        booking.save()

        validated_data["booking"] = booking
        travel_booking = TravelBooking.objects.create(**validated_data)
        travel_booking.save()
        return travel_booking

    def update(self, instance, validated_data):
        instance.agency = validated_data.get('agency')
        instance.dest_location = validated_data.get('dest_location')
        instance.initial_location = validated_data.get('initial_location')
        instance.travel_mode = validated_data.get('travel_mode')
        instance.save()







