# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from Actors.models import Tourist
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import status

# Create your views here.
from Security.serializer import EmailAuthenticationSerializer


class TouristLogin(ObtainAuthToken):
    def get_response(self, serializer):
        if serializer.is_valid() and serializer.validated_data['user']:
            user = serializer.validated_data['user']

            if(user):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token' : token.key,
                    'username' : user.username,
                    'email' : user.email,
                    'name' : f"{user.first_name} {user.last_name}",
                    "result": "success"
                }, status=status.HTTP_200_OK)

        return Response({"result": "error",
                         "message": "please provide required fields email , password"},
                        status=status.HTTP_401_UNAUTHORIZED)
        return Response({"result": "error", "message": "invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        # stream = BytesIO(request.body)
        # data = dict(JSONParser().parse(stream))
        data = request.data

        print("Authentication data")
        print(data)
        # Checking if the user is validating using email or username

        serializer = EmailAuthenticationSerializer(data=data, context={'request': request})
        return self.get_response(serializer)

        return Response({'error': "Invalid credentials", "result" : "unsuccessful"},
                        status=status.HTTP_401_UNAUTHORIZED)

