import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def fetch_news(api_key, query="technology", page_size=25):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&language=en&sortBy=publishedAt&apiKey={api_key}"
    resp = requests.get(url)
    articles = resp.json().get("articles", [])

    news_data = []
    for item in articles:
        content = item["title"] + " " + (item.get("description") or "")
        score = analyzer.polarity_scores(content)["compound"]
        news_data.append({
            "title": item["title"],
            "raw_text": item.get("description", ""),
            "url": item["url"],
            "thumbnail" : item['urlToImage'],
            "publishedAt": item["publishedAt"],
            "source": item["source"]["name"],
            "sentiment_score": score
         })

    return news_data