from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class MessageSerializers(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    @staticmethod
    def update(self, instance, validated_data):
        pass

    @staticmethod
    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.save()
        return message

    class Meta:
        model = Message
        fields = "__all__"
