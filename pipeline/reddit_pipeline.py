from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from scraper.reddit_scraper import fetch_subreddit_data

analyzer = SentimentIntensityAnalyzer()

def apply_sentiment(posts):
    for post in posts:
        post["sentiment"] = analyzer.polarity_scores(post["raw_text"])["compound"]
    return posts

def run_reddit_pipeline(sub="popular", limit=25, save=False):
    raw_data = fetch_subreddit_data(sub=sub, limit=limit)
    enriched = apply_sentiment(raw_data['raw_text'])
    df = pd.DataFrame(enriched)

    if save:
        df.to_csv(f"buzzboard/data/reddit_{sub}.csv", index=False)

    return df

# Demo run
if __name__ == "__main__":
    df = run_reddit_pipeline(limit=10)
    print(df[["title", "sentiment", "engagement_score"]])