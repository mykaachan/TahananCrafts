# Import required Django REST Framework and Django modules
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# Import serializers to handle request validation
from .serializers import RegisterSerializer, EmailSerializer, VerifyEmailOTPSerializer

# Import utility functions and models
from users.utils import generate_otp, send_otp_via_email
from users.models import OTP, EmailOTP

import random
from django.core.mail import send_mail


# ✅ Simple test to check if authentication-related endpoints are working
class TestAuthConnection(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "GET auth works!"})

    def post(self, request):
        return Response({"message": "POST auth works too!"})


# Registers a user directly (you will move this later to the verify step)
class RegisterView(APIView):
    def post(self, request):
        # Use the serializer to validate and save user data
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Creates the user in the DB
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Sends an OTP to a contact (email or phone)
class RequestOTPView(APIView):
    def post(self, request):
        contact = request.data.get('contact')  # Can be email or phone

        if not contact:
            return Response({'error': 'Contact is required'}, status=400)

        code = generate_otp()  # Create a random 6-digit OTP

        # Save the OTP and contact in the database
        OTP.objects.create(contact=contact, code=code)

        if '@' in contact:
            # If contact is email, send OTP via email
            send_otp_via_email(contact, code)
        else:
            # If contact is a phone number, you can plug in SMS function here
            # Example: send_sms(contact, code)
            pass

        return Response({'message': 'OTP sent successfully.'})


# Verifies if OTP entered is correct (for either email or phone)
class VerifyOTPView(APIView):
    def post(self, request):
        contact = request.data.get('contact')  # Get the contact again
        code = request.data.get('code')        # Get the entered OTP

        try:
            # Get the most recent OTP record for the contact
            otp_record = OTP.objects.filter(contact=contact, code=code, is_verified=False).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid code'}, status=400)

        # Check if OTP is expired using the model's helper function
        if otp_record.is_expired():
            return Response({'error': 'Code expired'}, status=400)

        # Mark the OTP as verified
        otp_record.is_verified = True
        otp_record.save()

        return Response({'message': 'Verified. You can now register.'})


# Sends OTP specifically to an email (used in email verification flow)
class SendEmailOTP(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Generate a random 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Save or update OTP in EmailOTP model
            EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp})

            # Send the OTP via email using Django's built-in function
            send_mail(
                subject="Your TahananCrafts OTP Code",
                message=f"Your OTP code is {otp}. It is valid for 5 minutes.",
                from_email="yourtahanancrafts@gmail.com",
                recipient_list=[email],
            )

            return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

        # Return validation errors if email is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Verifies the email OTP (used before final registration)
class VerifyEmailOTP(APIView):
    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                # Find the OTP record for the email
                record = EmailOTP.objects.get(email=email)

                if record.otp == otp:
                    # OTP matches, you may now register the user
                    record.delete()  # Optional: delete OTP after verification
                    return Response({'message': 'OTP verified. You may proceed to register.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

            except EmailOTP.DoesNotExist:
                return Response({'error': 'OTP not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
