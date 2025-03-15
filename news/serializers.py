from rest_framework import serializers

class NewsSerializer(serializers.Serializer):
    headline = serializers.CharField()
    source = serializers.CharField()
    published_at = serializers.CharField()

class SentimentSerializer(serializers.Serializer):
    asset = serializers.CharField()
    sentiment = serializers.CharField()

class TrendingTopicsSerializer(serializers.Serializer):
    trending_topics = serializers.ListField(child=serializers.CharField())
