# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User

from Actors.serializers import TouristSerializer, ConciergeSerializer
from .models import Tourist, Concierge

import json


from django.shortcuts import render
from django.db.models import F, Value

# Create your views here.

@api_view(["GET"])
def index(request):
    return Response({"Result" : "Success"})

class ConciergeListView(APIView):
    @staticmethod
    def get(self, request):
        concierge = Concierge.objects.values("city","street","contact", "price", "rating",).annotate(
            first_name = F("user__first_name"),
            last_name=F("user__last_name"),
            email=F("user__email")
        )
        return Response({"concierge_list" : concierge}, status=status.HTTP_200_OK)

    @staticmethod
    def post(self, request):
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)
        concierge_serializer = ConciergeSerializer(data=data);

        if concierge_serializer.is_valid():
            concierge, error = concierge_serializer.create(data)
            if concierge:
                message = f"{data['user']['first_name']} {data['user']['last_name']} record has been sucessfully inserted"
                return Response({"result": "success", "message": message, "data": concierge_serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)

        error = dict(concierge_serializer.errors)
        return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)


class ConciergeDetailView(APIView):

    @staticmethod
    def get(request, concierge_id):
        concierge = Concierge.objects.get(id = concierge_id);
        serializer = ConciergeSerializer(concierge);
        return Response(serializer.data)

    @staticmethod
    def update(request, concierge_id):
        concierge = Concierge.objects.get(id = concierge_id)
        conciergeSerializer = ConciergeSerializer(data=request.data)
        if(conciergeSerializer.is_valid()):
            concierge = conciergeSerializer.update(concierge, dict(conciergeSerializer.data))
            concierge.save()
        return Response({"result" : "success", "concierge" : conciergeSerializer.data})

    @staticmethod
    def delete(request, concierge_id):
        concierge = Concierge.objects.get(id = concierge_id)
        concierge.delete();
        return Response({"result":"success"})


class TouristListView(APIView):
    def get(self, request):
        tourist = Tourist.objects.values("country", "gender", "dob").annotate(
            first_name = F("user__first_name"),
            last_name = F("user__last_name"),
            email = F("user__email")
        )
        return Response(tourist, status=status.HTTP_200_OK)

    def post(self, request):
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)

        tourist_serializer = TouristSerializer(data=data)

        if tourist_serializer.is_valid():
            tourist, error = tourist_serializer.create(tourist_serializer.validated_data)
            if tourist:
                message = f"{data['user']['first_name']} {data['user']['last_name']} record has been sucessfully inserted"
                return Response({"result": "success", "message": message, "data": tourist_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "error", "message": error}, status=status.HTTP_200_OK)

        error = dict(tourist_serializer.errors)
        print(error)
        return Response({"result" : "error", "message" : error}, status=status.HTTP_200_OK)



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

def getUserData(data):
    user_data = data.pop('user')
    user_data = json.dumps(user_data)
    print("User data")
    print(user_data)
    print(type(user_data))
    data["user"] = user_data
    return data