from djoser.serializers import UserSerializer as BaseuserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']


class UserSerializer(BaseuserSerializer):
    class Meta(BaseuserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']