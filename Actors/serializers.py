from rest_framework import serializers

from django.contrib.auth.models import User, AbstractUser
from .models import Concierge, Tourist
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.last_name)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["username","first_name", "last_name", "email", "password"]


class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user, error = create_user(user_data)

        if user:
            validated_data['user'] = user
            tourist = Tourist(**validated_data)
            tourist.save()

            return tourist, None


        return None, error

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        # update the user super class data
        user = instance.user

        try:
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')

            instance.country = validated_data.get('country')
            instance.dob = validated_data.get('dob')
            instance.gender = validated_data('gender')

        except KeyError as e:
            print("Error message : ", e)
            pass

        user.save()
        instance.save()

        return instance

    class Meta:
        model = Tourist
        fields = "__all__"


class ConciergeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(validated_data):
        user_data = validated_data.pop('user')
        user, error = create_user(user_data)

        if user:
            validated_data['user'] = user
            concierge = Concierge(**validated_data)
            concierge.save()

            return concierge, None

        return None, error

    class Meta:
        model = Concierge
        fields = "__all__"

    def update(instance, validated_data):
        print("Printing the validated data")
        print(validated_data)
        user_data = validated_data.pop('user')
        # update the user super class data
        user = instance.user
        try:
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')

            instance.city = validated_data.get('city')
            instance.street = validated_data.get('street')
            instance.contact = validated_data.get('contact')
            instance.price = validated_data.get('price')
        except KeyError as e:
            print("Error message : ", e)
            pass

        user.save()
        instance.save()

        return instance

def create_user(user_data):
    print(user_data)
    try:
        if User.objects.get(email=user_data.get('email')):
            return None, "A user with that email address already exists"
    except User.DoesNotExist:
        pass
    user = User.objects.create(**user_data)
    user.set_password(user.password)
    user.save()
    return user, None
