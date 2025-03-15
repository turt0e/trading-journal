# 📝 Trading Journal API

## 📌 Overview
The **Trading Journal API** is a backend system designed for traders to **log, analyze, and optimize trading activities**.  
It provides features like trade tracking, risk management, market news fetching, sentiment analysis, and trade recommendations.

### 🌟 Features:
- **Trade Logging**: Log trades with entry/exit prices, volume, and type.
- **Performance Analysis**: Track win rate, profit/loss, and risk-reward ratios.
- **Market News Integration**: Fetch live news using **MarketAux API**.
- **Sentiment Analysis**: Analyze news sentiment with **NLTK (VADER) & TextBlob**.
- **Trade Recommendations**: Get trading insights based on past performance.
- **Data Export/Import**: Manage trade data in CSV/Excel format.

---

MARKETAUX_API_KEY="iJQNzKUed5cENRpztpNJFZvqESF6rSsWlhJPXsrM"

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/turt0e/trading-journal.git
cd trading-journal

# For Windows (CMD)
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

## If needed, install manually:
```sh
pip install django djangorestframework requests nltk textblob python-dotenv
```

