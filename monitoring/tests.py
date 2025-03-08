# backtest/tests.py

from django.test import TestCase
from trades.models import Trade
from .models import Recommendation

class SignalTests(TestCase):
    def test_recommendation_signal(self):
        # Create a trade with high PnL
        trade = Trade.objects.create(
            asset="EUR/USD",
            entry_price=1.1200,
            exit_price=1.1250,
            volume=1,
            trade_type="buy",
            pnl=150.0
        )

        # Check if a recommendation was created
        recommendation = Recommendation.objects.first()
        self.assertIsNotNone(recommendation)
        self.assertEqual(recommendation.asset, "EUR/USD")
        self.assertEqual(
            recommendation.reason,
            "High PnL observed in EUR/USD (buy) with PnL 150.0. This strategy has shown consistent profitability."
        )