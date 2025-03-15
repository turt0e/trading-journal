# trades/models.py
from django.db import models

class Trade(models.Model):
    asset = models.CharField(max_length=20)
    entry_price = models.DecimalField(max_digits=20, decimal_places=4)
    exit_price = models.DecimalField(max_digits=20, decimal_places=4)
    volume = models.DecimalField(max_digits=10, decimal_places=2)  # Number of lots
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)  # Default to 1 standard lot, tapos 1 lot is 100000units (for multiplier lang naman)
    trade_type = models.CharField(max_length=10)  # 'long' or 'short' positions
    pnl = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)  # PnL in currency units, usually USD to
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset} - {self.trade_type}"