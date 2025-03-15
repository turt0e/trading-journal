from django.db import models

class UserPreference(models.Model):
    preferred_assets = models.JSONField()  # Store as JSON
    risk_tolerance = models.CharField(max_length=50)

class Notification(models.Model):
    alert_type = models.CharField(max_length=50)
    asset = models.CharField(max_length=50)
    threshold = models.FloatField()