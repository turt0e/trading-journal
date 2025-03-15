from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, status
import pandas as pd
import io
from trades.models import Trade
from trades.serializers import TradeSerializer

class TradeHistoryView(generics.ListAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class DataExportView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        trades = Trade.objects.all()
        serializer = TradeSerializer(trades, many=True)
        df = pd.DataFrame(serializer.data)

        # Create CSV buffer
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()

        # Create HttpResponse with proper headers
        response = HttpResponse(csv_content, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="trades.csv"'

        return response

class DataImportView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        df = pd.read_csv(file)
        for _, row in df.iterrows():
            Trade.objects.create(
                asset=row['asset'],
                entry_price=row['entry_price'],
                exit_price=row['exit_price'],
                volume=row['volume'],
                trade_type=row['trade_type']
            )
        return Response({"message": "Data imported successfully."}, status=status.HTTP_201_CREATED)