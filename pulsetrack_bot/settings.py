
from pathlib import Path
import os


# Twilio Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'AC5cf85f8a3afbc20854857db032c311ea')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'f4bb08d1823f70bdfb6c3fcde2cc6aba')




TWILIO_PHONE_NUMBER = '+254748264302'  # Your purchased number
TWILIO_WHATSAPP_NUMBER = '+14155238886'  # Sandbox or business number


# Webhook security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')