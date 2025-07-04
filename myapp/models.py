from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    raw_message = models.TextField()
    sentiment_score = models.FloatField()
    detected_topics = models.JSONField(default=list)
    source_number = models.CharField(max_length=20, blank=True)
    media_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback ({self.timestamp:%Y-%m-%d %H:%M})"