from django.db import models
from trades.models import Trade 

class Recommendation(models.Model):
    asset = models.CharField(max_length=20)
    suggestion = models.CharField(max_length=10)  # e.g., 'Buy' or 'Sell'
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Alert(models.Model):
    asset = models.CharField(max_length=20)
    threshold = models.DecimalField(max_digits=10, decimal_places=4)
    alert_type = models.CharField(max_length=10)  # e.g., 'above' or 'below'
    created_at = models.DateTimeField(auto_now_add=True)

class BacktestRun(models.Model):
    strategy = models.CharField(max_length=50)  # e.g., 'SMC', 'Moving Average Crossover'
    total_trades = models.IntegerField()
    profit = models.DecimalField(max_digits=10, decimal_places=4)
    loss = models.DecimalField(max_digits=10, decimal_places=4)
    win_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)