
from twilio.rest import Client


def send_whatsapp_message(to_number, template_variables):
    account_sid = 'AC5cf85f8a3afbc20854857db032c311ea'
    auth_token = 'f4bb08d1823f70bdfb6c3fcde2cc6aba'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        content_sid='HX0c0e20764be209438385b8bb9bb7ec59',  
        content_variables=json.dumps(template_variables),
        from_='whatsapp:+14155238886',  # Twilio sandbox number
        to=f'whatsapp:{to_number}'
    )
    return message.sid