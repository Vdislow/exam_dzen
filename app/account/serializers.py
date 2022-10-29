from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password, ])
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_2', 'email', 'telegram_chat_id']

    def validate(self, data):
        if data['password'] != data['password_2']:
            raise ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            telegram_chat_id=validated_data['telegram_chat_id'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
