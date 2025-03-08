from django.db.models.signals import post_save
from django.dispatch import receiver
from trades.models import Trade
from .models import Recommendation

@receiver(post_save, sender=Trade)
def generate_recommendation(sender, instance, **kwargs):
    if instance.pnl > 100:  # Example condition
        Recommendation.objects.create(
            asset=instance.asset,
            suggestion="Consider this strategy",
            reason=f"High PnL observed in {instance.asset} ({instance.trade_type}) with PnL {instance.pnl}. This strategy has shown consistent profitability."
        )