import re
from django.core.mail import send_mail

#Converting 09 to +639
def normalize_phone_number(phone):
    phone = re.sub(r'\D', '', phone)  # Remove non-digit characters
    if phone.startswith('09'):
        return '+63' + phone[1:]
    elif phone.startswith('63'):
        return '+' + phone
    elif phone.startswith('+63'):
        return phone
    else:
        return phone  # fallback

### these are for Globe Lab
    ### Short Code 21665947 (Cross-telco: 225645947)
    ### APP ID 8xKaCoB59nuXkT8zEAi5KGuyRxKgCnpz
    ### APP SECRET 268b6c6a598edd95f6fb27a9b81c8864a0154522d4e815ffa5c22d1b0dc86d54


# OTP funtion - will generate otp and save to model and send to contact.
#send-email-OTP
def send_otp_email(email,code):
    send_mail(
        subject='Your TahananCrafts Verification Code',
        message=f'Your verification code is {code}. It expires in 5 minutes.',
        from_email='no-reply@tahanancrafts.com',
        recipient_list=[email],
    )

#send-contact-OTP
def send_otp_sms(contact, otp):
    # Simulate sending by printing
    print(f"OTP sent to {contact}: {otp}")
