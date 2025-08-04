from rest_framework import serializers
from users.models import CustomUser
from users.auth.validators import validate_email_or_phone, validate_password_strength
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from users.utils import normalize_phone_number



class RegisterSerializer(serializers.Serializer):
    contact = serializers.CharField(validators=[validate_email_or_phone])
    name = serializers.CharField()
    password = serializers.CharField(write_only=True, validators=[validate_password_strength])

    def validate_contact(self, value):
        if '@' in value:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already registered.")
        else:
            normalized_phone = normalize_phone_number(value)
            if CustomUser.objects.filter(phone=normalized_phone).exists():
                raise serializers.ValidationError("Phone already registered.")
            value = normalized_phone
        return value

    def create(self, validated_data):
        contact = validated_data.get("contact")
        name = validated_data.get("name")
        password = validated_data.get("password")

        # Distinguish between email and phone
        try:
            validate_email(contact)
            email = contact
            phone = None
        except ValidationError:
            email = None
            phone = contact

        user = CustomUser.objects.create_user(
            email=email,
            phone=phone,
            name=name,
            password=password
        )
        return user
