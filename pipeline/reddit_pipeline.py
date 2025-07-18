from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from scraper.reddit_scraper import fetch_subreddit_data

analyzer = SentimentIntensityAnalyzer()

def apply_sentiment(posts):
    for post in posts:
        post["sentiment"] = analyzer.polarity_scores(post["raw_text"])["compound"]
    return posts

def label_sentiment(s):
    if s >= 0.5: return "Positive"
    elif s <= -0.5: return "Negative"
    else: return "Neutral"

def get_comment_sentiment(post,top_n=10):
    post.comments.replace_more(limit=0)
    comments = post.comments[:top_n]

    scores = []
    for comment in comments:
        text = comment.body.strip()
        if text:
            score = analyzer.polarity_scores(text)["compound"]
            scores.append(score)

    if scores:
        return sum(scores) / len(scores) 
    return 0.0  

def run_reddit_pipeline(sub="popular", limit=25, save=False):
    raw_data = fetch_subreddit_data(sub=sub, limit=limit)
    enriched = apply_sentiment(raw_data)
    df = pd.DataFrame(enriched)
    df["sentiment_label"] = df["sentiment"].apply(label_sentiment)
    df["comment_sentiments"] = df["post_obj"].apply(lambda p: get_comment_sentiment(p, top_n=5))
    df['comment_sentiments_label'] = df['comment_sentiments'].apply(label_sentiment)
    if save:
        df.to_csv(f"buzzboard/data/reddit_{sub}.csv", index=False)

    return df

if __name__ == "__main__":
    df = run_reddit_pipeline(limit=10)
    print(df[["title", "sentiment_label", "engagement_score","domain","comment_sentiments_label"]])


