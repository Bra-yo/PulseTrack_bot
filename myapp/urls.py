# feedback/urls.py
from django.urls import path
from .twilio_integration import twilio_webhook

urlpatterns = [
    path('twilio/webhook/', twilio_webhook, name='twilio_webhook'),
]