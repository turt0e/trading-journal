import requests
import nltk
import re
from django.conf import settings
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Ensure NLTK's VADER model is available
nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

# MarketAux API Config
MARKETAUX_API_KEY = settings.MARKETAUX_API_KEY  
BASE_URL = "https://api.marketaux.com/v1/news/all"

# Common Stop Words
STOP_WORDS = {
    "the", "is", "to", "and", "in", "for", "on", "a", "of", "with", "at", "by", "an", 
    "be", "this", "that", "as", "it", "from", "can", "now"
}

def fetch_market_news(asset):
    """Fetch relevant news for a specific asset."""
    params = {
        "api_token": MARKETAUX_API_KEY,
        "search": asset,
        "language": "en",
        "limit": 5
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise error for HTTP failures
        data = response.json()

        print("🟢 DEBUG: Raw API Response:", data)  # 🔥 Debugging

        if "data" in data and isinstance(data["data"], list) and data["data"]:
            news_list = [
                {
                    "headline": article.get("title", "No headline available"),
                    "source": article.get("source", {}).get("name", "Unknown") if isinstance(article.get("source"), dict) else "Unknown",
                    "published_at": article.get("published_at", "Unknown date")
                }
                for article in data["data"]
            ]
            return {"news": news_list}

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: API request failed - {e}")  # 🔥 Debugging
        return {"news": {"message": "API request failed"}}

    return {"news": {"message": "No relevant news found for this asset"}}


def get_sentiment_score(text):
    """Combine VADER and TextBlob for better financial sentiment analysis"""
    vader_score = sia.polarity_scores(text)["compound"]
    textblob_score = TextBlob(text).sentiment.polarity
    combined_score = (vader_score + textblob_score) / 2  # Average both scores
    return combined_score


def analyze_news_sentiment(news_data):
    """Analyze sentiment of news articles."""
    
    print("🔍 DEBUG: Raw News Data:", news_data)  # Debugging log
    
    if not news_data or "news" not in news_data or not isinstance(news_data["news"], list):
        print("❌ DEBUG: No valid news data received")
        return {"sentiment": "No sentiment data available"}

    sentiment_scores = []

    for article in news_data["news"]:
        if isinstance(article, dict) and "headline" in article:
            text = article["headline"]
            score = get_sentiment_score(text)
            print(f"✅ DEBUG: Headline: {text} | Sentiment Score: {score}")
            sentiment_scores.append(score)

    # 🔥 Force a fallback sentiment score if we have news but no valid scores
    if not sentiment_scores:
        print("❌ DEBUG: No sentiment scores found, forcing Neutral")
        return {"sentiment": "Neutral"}  # Default fallback

    avg_score = sum(sentiment_scores) / len(sentiment_scores)
    print(f"📊 DEBUG: Average Sentiment Score: {avg_score}")

    # ✅ Apply improved sentiment thresholds
    if avg_score >= 0.40:
        sentiment_label = "Bullish"
    elif avg_score >= 0.20:
        sentiment_label = "Somewhat Bullish"
    elif avg_score > -0.20:
        sentiment_label = "Neutral"
    elif avg_score > -0.40:
        sentiment_label = "Somewhat Bearish"
    else:
        sentiment_label = "Bearish"

    print(f"🟢 FINAL SENTIMENT: {sentiment_label}")
    return {"sentiment": sentiment_label}



def get_trending_topics():
    """
    Identify trending topics by analyzing common words in news headlines.
    :return: Dictionary containing a list of trending topics.
    """
    params = {
        "api_token": MARKETAUX_API_KEY,
        "language": "en",
        "limit": 20
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract words from headlines
        headlines = [article.get("title", "") for article in data.get("data", [])]
        words = [word for headline in headlines for word in re.findall(r'\w+', headline.lower())]
        
        # Count most common words while filtering stop words
        trending_topics = [
            word for word, count in Counter(words).most_common(15) 
            if word.isalpha() and word not in STOP_WORDS
        ]

        return {"trending_topics": trending_topics[:10] if trending_topics else ["No trending topics found"]}

    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Failed to fetch trending topics - {e}")  # 🔥 Debugging log
        return {"trending_topics": ["API request failed"]}


news_data = {
    "news": [
        {"headline": "Apple stock soars to new highs"},
        {"headline": "Bitcoin crashes as investors panic"},
        {"headline": "Tesla announces major breakthrough in battery tech"},
    ]
}

sentiment = analyze_news_sentiment(news_data)
print("🟢 FINAL SENTIMENT:", sentiment)
