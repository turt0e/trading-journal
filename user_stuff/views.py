from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from .models import UserPreference, Notification
from trades.models import Trade
from .serializers import UserPreferenceSerializer, NotificationSerializer

class UserPreferenceCreateView(generics.CreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

class UserPreferenceListView(generics.ListAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

# Notifications
class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# Monthly Performance
class MonthlyPerformanceView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Get the current month and year
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # Filter trades for the current month and year
        trades = Trade.objects.filter(created_at__month=current_month, created_at__year=current_year)

        # Calculate total profit and loss
        total_profit = trades.aggregate(Sum('pnl'))['pnl__sum'] or 0.0
        total_loss = trades.filter(pnl__lt=0).aggregate(Sum('pnl'))['pnl__sum'] or 0.0

        # Prepare the response data
        response_data = {
            "month": now.strftime("%B %Y"),
            "total_profit": float(total_profit),
            "total_loss": float(total_loss),
        }
        return Response(response_data)

# Asset Performance
class AssetPerformanceView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Group trades by asset and calculate total profit/loss for each asset
        asset_performance = Trade.objects.values('asset').annotate(
            total_profit=Sum('pnl')
        )

        # Prepare the response data
        response_data = {asset['asset']: {
            "total_profit": float(asset['total_profit']) if asset['total_profit'] else 0.0
        } for asset in asset_performance}

        return Response(response_data)