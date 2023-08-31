from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.contrib.auth.hashers import make_password
from .models import MyUser as User
from django.contrib.auth import authenticate

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError({'error': 'Invalid credentials'})

        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        token = RefreshToken.for_user(instance)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","password", "role","gender","bio","walletAddress")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        username = attrs.get('username')

        if len(password) < 8:
            raise serializers.ValidationError({'error': 'Password must be at least 8 characters'})

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError({'error': 'Password must contain a combination of letters and numbers'})

        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({'error': 'Password must contain at least one uppercase letter'})

        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError({'error': 'Password must contain at least one digit'})

        if not re.search(r'[.!*\/#_]', password):
            raise serializers.ValidationError({'error': 'Password must contain at least one of the following characters: . ! * / # _'})

        if len(username) < 3:
            raise serializers.ValidationError({'error': 'Username must be at least 3 characters'})

        if not re.match(r'^[a-zA-Z0-9_.]+$', username):
            raise serializers.ValidationError({'error': 'Username can only contain letters, numbers, dots (.), and underscores (_)'})


        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        user = User.objects.create(password=hashed_password, **validated_data)
        return user

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return repr_

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
