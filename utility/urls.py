# urls.py
from django.urls import path
from .views import TradeHistoryView, DataExportView, DataImportView

urlpatterns = [
    path('utility/trade_history', TradeHistoryView.as_view(), name='trade_history'),
    path('utility/data_export', DataExportView.as_view(), name='data_export'),
    path('utility/data_import', DataImportView.as_view(), name='data_import'),
]