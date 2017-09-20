from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):

    auth_token = TokenSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'auth_token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        new_user = User(username=validated_data['username'], email=validated_data['email'])
        password = validated_data['password']
        new_user.set_password(password)
        new_user.save()
        return new_user


class UserDetailSerializer(serializers.ModelSerializer):

    auth_token = TokenSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'auth_token')
        extra_kwargs = {
            'password': {'write_only': True}
        }





