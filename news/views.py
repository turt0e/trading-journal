from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import fetch_market_news, analyze_news_sentiment, get_trending_topics
from django.http import JsonResponse

class MarketNewsView(APIView):
    def get(self, request):
        asset = request.GET.get("asset")
        if not asset:
            return Response({"error": "Asset parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        news_data = fetch_market_news(asset)
        return Response(news_data, status=status.HTTP_200_OK)

class MarketSentimentView(APIView):
    def get(self, request):
        asset = request.GET.get("asset")
        if not asset:
            return Response({"error": "Asset parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        news_data = fetch_market_news(asset)  # ✅ First, fetch news
        print("🔍 DEBUG: Fetched News Data:", news_data)  # 🔥 Debugging log

        sentiment_data = analyze_news_sentiment(news_data)  # ✅ Then, analyze sentiment
        return Response({"sentiment": sentiment_data}, status=status.HTTP_200_OK)

class MarketTrendingTopicsView(APIView):
    def get(self, request):
        trending_data = get_trending_topics()
        return Response(trending_data, status=status.HTTP_200_OK)

def market_news_view(request):
    asset = request.GET.get("asset", "AAPL")  # Default to AAPL if no asset is provided
    news_data = fetch_market_news(asset)

    print("🔍 DEBUG: News Data:", news_data)  # 🔥 Debugging
    return JsonResponse(news_data)