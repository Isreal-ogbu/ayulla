from django.contrib.auth import login, get_user_model, logout, authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from knox.views import LoginView
from .models import User
from rest_framework.views import APIView

from account.serializers import LoginSerializers, RegisterSerializer, UserSerializer


class LoginViewSet(GenericViewSet, LoginView):
    serializer_class = LoginSerializers
    permission_classes = [AllowAny,]

    def post(self, request, format=None):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = authenticate(request=request, email=serializers.validated_data['email'], password=serializers.validated_data['password'])
        login(request, user)
        return Response({"message": "success", "data": [user]}, status=status.HTTP_200_OK)


class LogoutViewSet(GenericViewSet):

    def post(self, request, format=None):
        logout(request.user)
        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)


class RegisterViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)