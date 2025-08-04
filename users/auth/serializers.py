from rest_framework import serializers
from users.models import CustomUser

class RegisterSerializer(serializers.Serializer):
    identifier = serializers.CharField()  # either email or phone
    name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        if '@' in value:
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already registered.")
        else:
            if CustomUser.objects.filter(phone=value).exists():
                raise serializers.ValidationError("Phone already registered.")
        return value

    def create(self, validated_data):
        identifier = validated_data.get("identifier")
        name = validated_data.get("name")
        password = validated_data.get("password")

        user = CustomUser.objects.create_user(identifier=identifier, name=name, password=password)
        return user
