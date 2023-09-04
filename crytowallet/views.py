from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny, IsAdminUser, SAFE_METHODS

from crytowallet.models import Crypto, UserCrytoWallet
from knox.auth import TokenAuthentication
from .serializers import CryptoSerializers, UserCryptoWalletSerializers, UserCrytoReportSerializers
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

SAFE_METHODS = ["GET", "POST"]

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CryptoViewset(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializers



class UserCrytoWalletViewSet(ModelViewSet):
    # buy, delete, change and view purchased cryto
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserCryptoWalletSerializers

    def get_queryset(self):
        return UserCrytoWallet.objects.filter(name=self.request.user)

class UserTotalCrypto(GenericAPIView):
    # Shows view and overview of the purchased crypto
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    queryset = UserCrytoWallet

    def get(self, request):
        query = UserCrytoWallet.objects.filter(name=self.request.user).values("crypto_currency__symbol").annotate(total=Sum("quantity"))
        lis = [i for i in query]
        serializer = UserCrytoReportSerializers(instance=lis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)