# trades/services.py
from django.db.models import Sum, Count, Avg, Max, Min
from .models import Trade

def calculate_trade_summary():
    total_trades = Trade.objects.count()
    total_profit = Trade.objects.filter(pnl__gt=0).aggregate(Sum('pnl'))['pnl__sum'] or 0
    total_loss = Trade.objects.filter(pnl__lt=0).aggregate(Sum('pnl'))['pnl__sum'] or 0
    total_pnl = Trade.objects.aggregate(Sum('pnl'))['pnl__sum'] or 0
    return {
        "total_trades": total_trades,
        "total_profit": total_profit,
        "total_loss": total_loss,
        "total_pnl": total_pnl
    }

def calculate_trade_performance():
    win_rate = Trade.objects.filter(pnl__gt=0).count() / Trade.objects.count() * 100
    avg_profit = Trade.objects.filter(pnl__gt=0).aggregate(Avg('pnl'))['pnl__avg'] or 0
    avg_loss = Trade.objects.filter(pnl__lt=0).aggregate(Avg('pnl'))['pnl__avg'] or 0
    return {
        "win_rate": win_rate,
        "average_profit": avg_profit,
        "average_loss": avg_loss
    }

def generate_trade_heatmap():
    heatmap = Trade.objects.values('asset').annotate(count=Count('id'))
    return {"heatmap": {item['asset']: item['count'] for item in heatmap}}