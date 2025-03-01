from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Trade
from .serializers import TradeSerializer
from .services import calculate_trade_summary, calculate_trade_performance, generate_trade_heatmap

class LogTrade(APIView):
    def post(self, request):
        serializer = TradeSerializer(data=request.data)
        if serializer.is_valid():

            entry_price = serializer.validated_data['entry_price']
            exit_price = serializer.validated_data['exit_price']
            volume = serializer.validated_data['volume'] 
            lot_size = serializer.validated_data.get('lot_size', 1.0)  

            total_volume = volume * lot_size
            pnl = (exit_price - entry_price) * total_volume

            trade = serializer.save(pnl=pnl)
            return Response({
                "message": "Trade logged successfully.",
                "trade_id": trade.id,
                "pnl": pnl  # Include PnL in the response
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class TradeSummary(APIView):
    def get(self, request):
        summary = calculate_trade_summary()
        return Response(summary)

class TradePerformance(APIView):
    def get(self, request):
        performance = calculate_trade_performance()
        return Response(performance)

class TradeHeatmap(APIView):
    def get(self, request):
        heatmap = generate_trade_heatmap()
        return Response(heatmap)

class PnLAnalysis(APIView):
    def get(self, request):
        pnl = calculate_pnl()
        return Response(pnl)

class DeleteTrade(APIView):
    def delete(self, request, trade_id):
        try:
            trade = Trade.objects.get(id=trade_id)
            trade.delete()
            return Response({"message": "Trade deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Trade.DoesNotExist:
            return Response({"message": "Trade not found."}, status=status.HTTP_404_NOT_FOUND)