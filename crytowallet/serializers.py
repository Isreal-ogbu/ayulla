from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

from crytowallet.models import Crypto, UserCrytoWallet


class CryptoSerializers(ModelSerializer):

    class Meta:
        model= Crypto
        fields = "__all__"

class UserCryptoWalletSerializers(ModelSerializer):
    name = serializers.HiddenField(default=serializers.CurrentUserDefault())
    crypto_currency = serializers.SlugRelatedField(slug_field="symbol", queryset= Crypto.objects.all())

    class Meta:
        model = UserCrytoWallet
        fields = [
            "name",
            "crypto_currency",
            "quantity",
            "date_created"
        ]


class UserCrytoReportSerializers(Serializer):
    crypto_currency__symbol = serializers.CharField(max_length=100)
    total = serializers.CharField(max_length=100)
