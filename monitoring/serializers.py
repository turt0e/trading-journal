from rest_framework import serializers
from .models import Recommendation, Alert, BacktestRun
from trades.models import Trade

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'asset', 'suggestion', 'reason', 'created_at']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'asset', 'threshold', 'alert_type', 'created_at']

class BacktestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = BacktestRun
        fields = ['id', 'strategy', 'total_trades', 'profit', 'loss', 'win_rate', 'created_at']

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'asset', 'entry_price', 'exit_price', 'trade_type', 'pnl', 'volume', 'created_at']