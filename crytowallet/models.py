from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class Wallet(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=3)
    current_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()


class UserCrytoWallet(models.Model):
    name = models.ForeignKey(User, related_name='cryto_user', on_delete=models.CASCADE)
    crypto_currency = models.ForeignKey(Wallet, on_delete=models.CASCADE)
