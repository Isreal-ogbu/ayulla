from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class Crypto(models.Model):
    # General cryto details
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=3)
    current_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class UserCrytoWallet(models.Model):
    # User cryto account
    name = models.ForeignKey(User, related_name='usercryptowallet', on_delete=models.CASCADE)
    crypto_currency = models.ForeignKey(Crypto, related_name='usercryptowallet', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
