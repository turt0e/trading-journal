from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recommendation, Alert, BacktestRun
from trades.models import Trade
from .serializers import RecommendationSerializer, AlertSerializer, BacktestRunSerializer, TradeSerializer

class RecommendationView(APIView):
    def get(self, request):
        # Get all trades
        trades = Trade.objects.all()

        # Calculate average PnL
        total_pnl = sum(trade.pnl for trade in trades)
        average_pnl = total_pnl / len(trades) if trades else 0

        low_pnl_threshold = 0

        if average_pnl <= low_pnl_threshold:
            # Find trades with high PnL (e.g., top 10% of trades)
            high_pnl_trades = Trade.objects.filter(pnl__gt=0).order_by('-pnl')[:5]  # Top 5 high PnL trades
            recommendations = []
            for trade in high_pnl_trades:
                recommendations.append({
                    "asset": trade.asset,
                    "suggestion": "Consider this strategy",
                    "reason": f"High PnL observed in {trade.asset} ({trade.trade_type}) with PnL {trade.pnl}. This strategy has shown consistent profitability."
                })
        else:
            # If the user is performing well, suggest niya what to do basically 
            recommendations = [
                {
                    "asset": "EUR/USD",
                    "suggestion": "Hold",
                    "reason": "Your current strategy is performing well. No significant changes are recommended."
                }
            ]
        return Response({'recommendations': recommendations})          

class AlertView(APIView):
    def post(self, request):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Alert set successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlertListView(APIView):
    def get(self, request):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response({'alerts': serializer.data})

class BacktestView(APIView):
    def post(self, request):
        strategy = request.data.get('strategy')
        trades_data = request.data.get('trades')  # List of trades from the request

        # Validate input
        if not strategy or not trades_data:
            return Response({"error": "Strategy and trades data are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create trades from the provided data
        trades = [
            Trade(
                asset=trade.get('asset'),
                entry_price=trade.get('entry_price'),
                exit_price=trade.get('exit_price'),
                trade_type=trade.get('trade_type'),  # 'long' or 'short'
                pnl=trade.get('pnl', 0.0),  # Default PnL is 0.0
                volume=trade.get('volume', 1)  # Default volume is 1
            )
            for trade in trades_data
        ]

        # Save trades to the database
        Trade.objects.bulk_create(trades)

        # Calculate backtest results
        total_trades = len(trades)
        profit = sum(trade.pnl for trade in trades if trade.pnl > 0)  # Total profit from winning trades
        loss = abs(sum(trade.pnl for trade in trades if trade.pnl < 0))  # Total loss from losing trades
        win_rate = (sum(1 for trade in trades if trade.pnl > 0) / total_trades) * 100 if total_trades else 0  # Win rate as a percentage

        # Save backtest results
        backtest_run = BacktestRun(
            strategy=strategy,
            total_trades=total_trades,
            profit=profit,
            loss=loss,
            win_rate=win_rate
        )
        backtest_run.save()

        # Serialize and return the backtest results and trades
        backtest_run_serializer = BacktestRunSerializer(backtest_run)
        trade_serializer = TradeSerializer(trades, many=True)

        return Response({
            'backtest_results': backtest_run_serializer.data,
            'trades': trade_serializer.data
        }, status=status.HTTP_201_CREATED)