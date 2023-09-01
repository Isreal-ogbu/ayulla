from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from account.models import User


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        self.password_check(user)
        if user is None:
            raise serializers.ValidationError("Invalid Email and password")
        attrs["user"] = user
        return attrs

    def password_check(self, user):
        if user.password is None:
            raise serializers.ValidationError("User is required to set password, check your email")


class RegisterSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        read_only_fields = ["username"]


class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        exclude = ['password']