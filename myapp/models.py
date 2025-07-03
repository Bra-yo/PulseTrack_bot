from django.db import models
from django.contrib.auth.models import User




class Feedback(models.Model):
    message = models.TextField()
    sentiment_score = models.FloatField()  # -1.0 (negative) to 1.0 (positive)
    detected_topics = models.JSONField(default=list)  # e.g., ["workload", "manager"]
    timestamp = models.DateTimeField(auto_now_add=True)

    # feedback/models.py
    from django.db import models
    from django.contrib.auth.models import User

    class Department(models.Model):
        name = models.CharField(max_length=100)

        def __str__(self):
            return self.name

    class Employee(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
        phone = models.CharField(max_length=20, unique=True)
        department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.phone

    class FeedbackConfig(models.Model):
        department = models.ForeignKey(Department, on_delete=models.CASCADE)
        frequency = models.CharField(max_length=20, choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
        ], default='weekly')
        questions = models.JSONField(default=list)  # Store list of question strings

        def __str__(self):
            return f"{self.department} - {self.frequency}"