from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Feedback)
def handle_critical_feedback(sender, instance, created, **kwargs):
    if created and instance.sentiment_score < -0.7:
        # Send email alert
        subject = f"Critical Feedback Alert: {instance.department}"
        message = f"""
        Critical feedback detected in {instance.department} department.

        Message: {instance.message}
        Sentiment Score: {instance.sentiment_score}
        Detected Topics: {', '.join(instance.detected_topics)}

        Time: {instance.timestamp}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin[0] for admin in settings.ADMINS],
            fail_silently=False,
        )

        # Optional: Send WhatsApp alert to HR
        if hasattr(settings, 'HR_PHONE_NUMBER'):
            from .twilio_utils import send_whatsapp_message
            send_whatsapp_message(
                settings.HR_PHONE_NUMBER,
                {
                    "1": "CRITICAL FEEDBACK ALERT",
                    "2": instance.department.name,
                    "3": instance.message[:100] + "..." if len(instance.message) > 100 else instance.message
                }
            )
            #   instance.message}")   - Hii nmeeka hivyo though we can work it out later instead ya kutuma gmail kwa HR ikuange inamtumia direct kwa whatsapp