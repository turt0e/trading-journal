from django.urls import path
from .views import MarketNewsView, MarketSentimentView, MarketTrendingTopicsView

urlpatterns = [
    path("market/news/", MarketNewsView.as_view(), name="market_news"),
    path("market/news/sentiment/", MarketSentimentView.as_view(), name="market_news_sentiment"),
    path("market/news/trending/", MarketTrendingTopicsView.as_view(), name="market_news_trending"),
]
