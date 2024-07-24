from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=1, max_length=50)
    password = serializers.CharField(min_length=4, max_length=50)
    confirm_password = serializers.CharField(min_length=4, max_length=50)
    email = serializers.EmailField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError("Passwords don't match")
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=1, max_length=50)
    password = serializers.CharField(min_length=4, max_length=50)


class SMScodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)
