from rest_framework.serializers import Serializer, ModelSerializer

from crytowallet.models import Wallet, UserCrytoWallet


class WallletSerializers(ModelSerializer):

    class Meta:
        model= Wallet
        fields = "__all__"

class UserCryptoWallet(Serializer):
    wallet = wallet
    class Meta:
        model = UserCrytoWallet
        fields = ["user", "wallet"]

