import praw
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def clean_text(text):
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

def fetch_subreddit_data(sub="popular", limit=10):
    posts = []
    for post in reddit.subreddit(sub).hot(limit=limit):
        raw_text = post.selftext if post.selftext else post.title
        cleaned = clean_text(raw_text)
        posts.append({
            "source":"reddit",
            "title": post.title,
            "raw_text": cleaned,
            "score": post.score,
            "num_comments": post.num_comments,
            "post_obj" : post,
            "publishedAt": datetime.utcfromtimestamp(post.created_utc).isoformat(),
            "url": post.url,
            "thumbnail": post.thumbnail,
            "engagement_score": post.score + post.num_comments
        })
    return posts