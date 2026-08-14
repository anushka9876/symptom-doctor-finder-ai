from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_appointment_sms(to_phone, hospital_name, specialty):
    if not to_phone:
        return False

    try:
        phone = str(to_phone).strip()
        if phone.startswith('0'):
            phone = '+91' + phone[1:]
        elif not phone.startswith('+'):
            phone = '+91' + phone

        # Real Twilio code — requires DLT registration for Indian numbers
        # Uncomment below for international numbers or after DLT registration
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(
        #     body=f"Your appointment at {hospital_name} for {specialty} is confirmed via MediCheck.",
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=phone
        # )

        # Mock SMS for development (Indian numbers require DLT registration)
        logger.info(f"SMS to {phone}: Appointment at {hospital_name} for {specialty} confirmed.")
        print(f"[SMS] To: {phone} | Hospital: {hospital_name} | Specialty: {specialty}")
        return True

    except Exception as e:
        print(f"SMS error: {e}")
        return False