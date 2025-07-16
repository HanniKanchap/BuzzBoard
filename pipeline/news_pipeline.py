import pandas as pd
from scraper.news_scraper import fetch_news
import os
from dotenv import load_dotenv

load_dotenv()

def label_sentiment(s):
    if s >= 0.5: return "Positive"
    elif s <= -0.5: return "Negative"
    else: return "Neutral"

q = "AI"
news_raw = fetch_news(api_key=os.getenv("NEWS_API"), query=q, page_size=50)
df_news = pd.DataFrame(news_raw)
df_news['domain'] = q
df_news["sentiment_label"] = df_news["sentiment_score"].apply(label_sentiment)
print(df_news[['title','source','sentiment_score','sentiment_label']])