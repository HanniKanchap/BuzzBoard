import pandas as pd
from scraper.news_scraper import fetch_news
import os
from dotenv import load_dotenv

load_dotenv()

def label_sentiment(s):
    if s >= 0.5: return "Positive"
    elif s <= -0.5: return "Negative"
    else: return "Neutral"

def news_df_finalize(query):
    news_raw = fetch_news(api_key=os.getenv("NEWS_API"), query=query, page_size=25)
    df_news = pd.DataFrame(news_raw)
    df_news['domain'] = query
    df_news["sentiment_label"] = df_news["sentiment_score"].apply(label_sentiment)
    return df_news
