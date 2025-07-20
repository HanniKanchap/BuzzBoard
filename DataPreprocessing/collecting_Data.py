import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pipeline.news_pipeline import news_df_finalize
from pipeline.reddit_pipeline import run_reddit_pipeline
import pandas as pd

domains = {
    "Technology": ["technology", "Futurology", "gadgets"],
    "Healthcare": ["health", "medicine", "AskDocs"],
    "Climate": ["climate", "environment", "climatechange"],
    "Politics": ["politics", "PoliticalDiscussion"],
    "Economy": ["economy", "finance", "investing"],
    "Education": ["education", "Teachers", "GradSchool"],
    "Space": ["space", "spacex", "astronomy"],
    "Defense": ["Military", "CombatFootage", "geopolitics"],
    "Media": ["movies", "television", "Entertainment"],
    "Privacy": ["privacy", "netsec", "privacytoolsIO"],
    "Law": ["legaladvice", "law", "Ask_Lawyers"],
    "Social Movements": ["activism", "socialism", "TwoXChromosomes"],
    "Transportation": ["cars", "urbanplanning", "electricvehicles"],
    "Food": ["food", "Cooking", "vegan"],
    "Entertainment": ["popculture", "music", "gaming"],
    "Science": ["science", "AskScience", "EverythingScience"],
    "Artificial Intelligence": ["ChatGPT", "MachineLearning", "AI"],
    "Workforce": ["jobs", "WorkReform", "careerguidance"],
    "Mental Health": ["mentalhealth", "depression", "Anxiety"],
    "Disasters": ["naturaldisasters", "worldnews", "weather"]
}

def get_subdomains(dom):
    return domains[dom]


if __name__ == "__main__":
    
    reddit_df = pd.DataFrame()
    print("Working on it")
    for cat, subreddits in domains.items():
        for sub in subreddits:
            print(f"⏳ Fetching: r/{sub} under domain [{cat}]")
            try:
                df = run_reddit_pipeline(sub, cat)
                reddit_df = pd.concat([reddit_df, df], ignore_index=True)
                df.to_csv('data/RedditData.csv', index=False, mode="a")
            except Exception as e:
                print(f"❌ Error with r/{sub}: {e}")

    print("\n✅ Done.")
    print("***************")
    print(reddit_df)

    ## News API data

    # news_df = pd.DataFrame([])
    # print("Working on it")

    # for domain in domains.keys():
    #     df = news_df_finalize(domain)
    #     news_df = pd.concat([news_df,df],ignore_index= True)
    #     print("still working")

    # news_df.to_csv('data/NewsData.csv', index=False)
    # print(news_df)
