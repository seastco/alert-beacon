import os
import logging
from phonenumbers import parse, is_valid_number

logger = logging.getLogger(__name__)

STATIC_API_KEY = os.getenv('STATIC_API_KEY')

class ValidationError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

def validate_request(event):
    api_key = event.get('headers', {}).get('x-api-key')
    if not api_key:
        raise ValidationError(401, 'Unauthorized: API key is required')

    if api_key != STATIC_API_KEY:
        raise ValidationError(401, 'Unauthorized: Invalid API key')

    phone_number = event.get('phone_number')
    if not phone_number:
        raise ValidationError(400, 'Phone number is required')

    if not is_valid_number(parse(phone_number, "US")):
        raise ValidationError(400, 'Invalid phone number')

    return phone_number