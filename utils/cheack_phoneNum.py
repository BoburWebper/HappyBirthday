import phonenumbers
from phonenumbers import NumberParseException


def is_valid_phone_number(phone_number, region="UZB"):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, region)
        # Check if the parsed number is valid
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        # If parsing fails, the number is invalid
        return False
