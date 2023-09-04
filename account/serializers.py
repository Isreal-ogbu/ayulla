from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Referral

User = get_user_model()


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")
        user = authenticate(self.context['request'], email=email, password=password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise Exception(msg)
        attrs['user'] = user
        return attrs


class RegisterSerializer(ModelSerializer):

    @transaction.atomic
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = super().create(validated_data)
        # Each user will have only one referral link
        Referral.objects.create(user=user)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_phone_number(self, value):
        if len(value) > 11 or len(value) < 11 or value[0] != "0":
            msg = _('Enter a valid phone number starting with 0...')
            raise Exception(msg)
        return value

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password"]
        read_only_fields = ["username"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

# This serializers are for the email verification, but you will need an

class PasswordRecoveryserialisers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    @transaction.atomic
    def validate(self, attrs):
        user = None
        email = attrs.get("email").lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None
            msg = _('Unable to find user with provided credentials.')
            raise Exception(msg)
        password, confirm_password = attrs.get('password'), attrs.get('confirm_password')
        if password != confirm_password:
            msg = _('Pasword Mismatch. Check password again...')
            raise Exception(msg)
        user.set_password(password)
        attrs["user"] = user
        user.save()
        return attrs


class ReferralSerialiserizerToken(serializers.Serializer):
    token = serializers.UUIDField()

    def validate(self, attrs):
        token = attrs.get('token')
        referal=None
        try:
            referal = Referral.objects.get(token__iexact=token)
        except Referral.DoesNotExist:
            referal = None
            msg = _('Your referral link is invalid...')
            raise Exception(msg)
        attrs['user'] = referal
        referal.referral_count +=1
        referal.save()
        return attrs