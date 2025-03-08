from django.urls import path
from .views import RecommendationView, AlertView, AlertListView, BacktestView

urlpatterns = [
    path('trades/recommendations', RecommendationView.as_view(), name='recommendations'),
    path('trades/alerts', AlertView.as_view(), name='set_alert'),
    path('trades/alerts/list', AlertListView.as_view(), name='list_alerts'),
    path('trades/backtest', BacktestView.as_view(), name='backtest'),
]