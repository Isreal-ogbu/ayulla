from django.contrib.auth import login, get_user_model, logout, authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from knox.views import LoginView, LogoutView

from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from ayullaTest import settings
from .models import Referral


from account.serializers import LoginSerializers, RegisterSerializer, UserSerializer, PasswordRecoveryserialisers

User = get_user_model()

class LoginViewSet(GenericViewSet, LoginView):
    serializer_class = LoginSerializers
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
            if response.status_code != 200:
                raise Exception(response.data['error'])
            response = Response({
                "status": 'success',
                "data": [response.data, UserSerializer(instance=user).data],
                "message": 'success'
            }, status=status.HTTP_200_OK)
            return response
        except Exception as e:
            return Response({
                "status": 'failed',
                "data": [],
                "message": f"Error - {e}"
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(GenericViewSet, LogoutView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def logout(self, request):
        super().post(request, format=None)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            logout(request)

        response = Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK,
            )
        return response

    def post(self, request, *args, **kwargs):
        return self.logout(request)


class RegisterViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class PasswordRecoveryView(GenericViewSet):
    serializer_class = PasswordRecoveryserialisers
    # This feature is lazy. I would have implemented a message system to email of phone. This is just developed because of the test
    # The user is not authenticated, please note.
    def post(self, request, format=None):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data['user']
            return Response({
                    "status": 'success',
                    "data": [UserSerializer(instance=data).data],
                    "message": 'success'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 'failed',
                "data": [],
                "message": f"Error - {e}"
            }, status=status.HTTP_401_UNAUTHORIZED)


class ReferralView(GenericViewSet):
    # This will be a post request that will be authenticated and the operations count will be updated for the user
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, code, format=None):
        try:
            serializer = self.get_serializer(data=code)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data['user']
            return Response({
                    "status": 'success',
                    "data": [],
                    "message": 'success'
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 'failed',
                "data": [],
                "message": f"Error - {e}"
            }, status=status.HTTP_401_UNAUTHORIZED)

class GetUserReferalLink(GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        referal = Referral.objects.get(user=self.request.user)
        return Response({
                    "status": 'success',
                    "data": [{
                        "referal link": f"http://127.0.0.1:8000/referal/{referal.link}/welcome"
                    }],
                    "message": 'success'
                }, status=status.HTTP_200_OK)

