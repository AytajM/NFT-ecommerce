from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from .models import MyUser

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            return Response({
                'refresh': str(token),
                'access': str(token.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersListView(generics.ListAPIView):
    serializer_class = UsersListSerializer

    def get_queryset(self):
        return MyUser.objects.filter(role='artist').exclude(is_superuser=True)

class UserView(generics.ListAPIView):
    serializer_class = UsersListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.exclude(is_superuser=True)

class FollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            current_user = request.user  
            target_user = get_object_or_404(MyUser, id=user_id) 

            if current_user == target_user:
                return Response({"message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

            current_user.following.add(target_user) 

            return Response({"message": f"You have successfully followed {target_user.username}."}, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            current_user = request.user 
            target_user = get_object_or_404(MyUser, id=user_id) 

            current_user.following.remove(target_user) 

            return Response({"message": f"You have successfully unfollowed {target_user.username}."}, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)