from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from tasks.models import ToDo


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'created_at', 'completed', 'user']
        read_only_fields = ['id', 'created_at', 'user']
