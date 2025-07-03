from django.db.models.signals import post_save
from django.dispatch import receiver

from myapp.models import Feedback


def send_email_alert(param):
    pass


@receiver(post_save, sender=Feedback)
def alert_hr(sender, instance, **kwargs):
    if instance.sentiment_score < -0.7:
        send_email_alert(f"Critical feedback: {instance.message}")