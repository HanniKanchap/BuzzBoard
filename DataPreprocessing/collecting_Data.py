import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.news_pipeline import news_df_finalize
from pipeline.reddit_pipeline import run_reddit_pipeline
import pandas as pd

domains = [
    "Technology",
    "Healthcare",
    "Climate",
    "Politics",
    "Economy",
    "Education",
    "Space",
    "Defense",
    "Media",
    "Privacy",
    "Law",
    "Social Movements",
    "Transportation",
    "Food",
    "Entertainment",
    "Science",
    "Artificial Intelligence",
    "Workforce",
    "Mental Health",
    "Disasters"
]

#news_df = pd.DataFrame([])
reddit_df = pd.DataFrame([])
print("Working on it")
for domain in domains:
     # df = news_df_finalize(domain)
    #news_df = pd.concat([news_df,df],ignore_index= True)
    print("still working")
    df = run_reddit_pipeline(domain)
    reddit_df = pd.concat([reddit_df,df],ignore_index= True)

## news_df.to_csv('data/NewsData.csv', index=False)
reddit_df.to_csv('data/RedditData.csv', index=False)

## print(news_df)
print('***************')
print(reddit_df)
