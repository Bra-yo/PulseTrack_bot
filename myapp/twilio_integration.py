# feedback/twilio_integration.py
import json
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .models import Feedback  # Your Feedback model
from .utils import analyze_sentiment, extract_topics  # Your analysis utils

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Twilio client
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

QUESTION_TEMPLATES = {
    "biweekly_checkin": "HXb5b62575e6e4ff6129ad7c8efe1f983e",}

default_vars = {
        "1": employee.first_name,} #make kwa model yako employee aki sign up kuna kitu inaitwa first name plz

 
template_vars = {**default_vars, }

to_number = employee.phone_number  # Na bado ueke phone number kwa model yako ya employee

def send_whatsapp_message(to_number, template_vars):
    """Send WhatsApp message using Twilio template"""
    try:
        message = twilio_client.messages.create(
            content_sid=biweekly_checkin,
            content_variables=json.dumps(template_vars),
            from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{to_number}'
        )
        logger.info(f"Message sent to {to_number}: SID={biweek_checkin}")
        return message.sid
    except TwilioRestException as e:
        logger.error(f"Twilio send error: {e.msg} (Code {e.code})")
        return None


def send_sms(to_number, message_body):
    """Send SMS fallback message"""
    try:
        message = twilio_client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        logger.info(f"SMS sent to {to_number}: {message_body[:20]}...")
        return message.sid
    except TwilioRestException as e:
        logger.error(f"SMS send error: {e.msg}")
        return None


@csrf_exempt
def twilio_webhook(request):
    """Handle incoming Twilio messages"""
    try:
        # Extract message data
        message_body = request.POST.get('Body', '').strip()
        from_number = request.POST.get('From', '')
        media_url = request.POST.get('MediaUrl0', None)

        if not message_body:
            logger.warning(f"Empty message from {from_number}")
            return HttpResponse("Empty message ignored", status=200)

        # Process message
        sentiment = analyze_sentiment(message_body)
        topics = extract_topics(message_body)

        # Store feedback
        Feedback.objects.create(
            raw_message=message_body,
            sentiment_score=sentiment,
            detected_topics=topics,
            source_number=from_number,
            media_url=media_url
        )

        # Send acknowledgment
        if 'whatsapp' in from_number:
            send_whatsapp_message(
                to_number=from_number,
                template_sid=settings.TWILIO_ACK_TEMPLATE,
                template_variables={"1": "received"}
            )
        else:
            send_sms(from_number, "✓ Feedback received. Thank you!")

        return HttpResponse(status=200)

    except Exception as e:
        logger.exception("Webhook processing failed")
        # Fallback error response
        try:
            if 'whatsapp' in from_number:
                send_whatsapp_message(
                    to_number=from_number,
                    template_sid=settings.TWILIO_ERROR_TEMPLATE,
                    template_variables={"1": "technical issue"}
                )
            else:
                send_sms(from_number, "⚠️ System error. Your feedback wasn't saved.")
        except Exception:
            pass

        return HttpResponse(status=500)