import re

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
