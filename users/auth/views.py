# Import required Django REST Framework and Django modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.cache import cache

# Import serializers to handle request validation
from .serializers import RequestOTPSerializer, VerifyOTPSerializer

# Import utility functions and models
from users.utils import send_otp_email, send_otp_sms, normalize_phone_number
from users.models import CustomUser

import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Simple test to check if authentication-related endpoints are working
class TestAuthConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "GET auth works!"})

    def post(self, request):
        return Response({"message": "POST auth works too!"})

# Sends an OTP to a contact (email or phone)
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.validated_data['contact']
            name = serializer.validated_data['name']
            password = serializer.validated_data['password']

            # Determine contact type
            try:
                validate_email(contact)
                contact_type = 'email'
            except ValidationError:
                contact_type = 'phone'
                contact = normalize_phone_number(contact)

            otp = str(random.randint(100000, 999999))

            # Store registration data and OTP in cache (expires in 5 min)
            cache.set(f"reg_{contact}", {
                "name": name,
                "contact": contact,
                "password": password,
                "otp": otp,
                "contact_type": contact_type
            }, timeout=300)

            # TODO: Send OTP via email or SMS here
            if contact_type == 'email':
                send_otp_email(contact, otp)
            else:
                send_otp_sms(contact, otp)

            return Response({"message": "OTP sent successfully. Enter OTP to verify email / contact number."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Verifies if OTP entered is correct (for either email or phone)
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.validated_data['contact']

            # Normalize contact for cache lookup
            if '@' in contact:
                normalized_contact = contact
            else:
                normalized_contact = normalize_phone_number(contact)

            otp = serializer.validated_data['otp']

            reg_data = cache.get(f"reg_{normalized_contact}")
            if not reg_data or reg_data['otp'] != otp:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            # Create user
            if reg_data['contact_type'] == 'email':
                user = CustomUser.objects.create_user(
                    email=reg_data['contact'],
                    name=reg_data['name'],
                    password=reg_data['password']
                )
            else:
                user = CustomUser.objects.create_user(
                    phone=reg_data['contact'],
                    name=reg_data['name'],
                    password=reg_data['password']
                )

            cache.delete(f"reg_{normalized_contact}")
            return Response({"message": "Successfully registered."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)