from django.urls import path
from .views import LogTrade, TradeSummary, TradePerformance, TradeHeatmap, DeleteTrade

urlpatterns = [
    path('trades/log', LogTrade.as_view(), name='log_trade'),
    path('trades/summary', TradeSummary.as_view(), name='trade_summary'),
    path('trades/performance', TradePerformance.as_view(), name='trade_performance'),
    path('trades/heatmap', TradeHeatmap.as_view(), name='trade_heatmap'),
    path('trades/delete/<int:trade_id>', DeleteTrade.as_view(), name='delete_trade'),
]