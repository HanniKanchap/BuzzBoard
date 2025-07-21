import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from pipeline.Clean_LiveData import clean_NewsAPIData

# --- Config ---
st.set_page_config(page_title="BuzzBoard Visualizer", page_icon="📊", layout="wide")
st.markdown("## 📊 BuzzBoard | Visual Insights")
st.markdown("Explore emotional intelligence from cached Reddit and NewsAPI data.")

domains = [
    "Technology", "Healthcare", "Climate", "Politics", "Economy", "Education", "Space",
    "Defense", "Media", "Privacy", "Law", "Social Movements", "Transportation", "Food",
    "Entertainment", "Science", "Artificial Intelligence", "Workforce", "Mental Health", "Disasters"
]

# --- Platform Selector ---
platform = st.radio("🌐 Select Platform", ["Reddit", "NewsAPI"], horizontal=True)

# --- Load Cached Data ---
def load_data(platform):
    if platform == "Reddit":
        path = Path(__file__).resolve().parent.parent / "data" / "Cleaned_RedditData.csv"
        df = pd.read_csv(path)
        

    else:
        path = Path(__file__).resolve().parent.parent / "data" / "NewsData.csv"
        raw = pd.read_csv(path)
        df = clean_NewsAPIData(raw)

    return df

df = load_data(platform)

# --- Sentiment by Domain ---
sentiment_df = (
    df.groupby(["domain", "sentiment_label"])
    .size()
    .reset_index(name="count")
)

fig_sentiment = px.bar(
    sentiment_df, x="domain", y="count", color="sentiment_label",
    title="🧠 Sentiment Distribution by Domain",
    color_discrete_map={"Positive": "#08FDD8", "Neutral": "#888", "Negative": "#EFB0B0"},
)
st.plotly_chart(fig_sentiment, use_container_width=True)

# --- Reddit-Only Visuals ---
if platform == "Reddit":
    if "engagement_score" in df.columns:
        engagement_df = (
            df.groupby("domain")["engagement_score"]
            .mean()
            .reset_index()
            .sort_values(by="engagement_score", ascending=False)
        )
        fig_engagement = px.bar(
            engagement_df, x="domain", y="engagement_score",
            title="🔥 Avg Reddit Engagement by Domain",
            color="domain", color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_engagement, use_container_width=True)

    if "comment_sentiments_label" in df.columns:
        comment_df = (
            df.groupby(["domain", "comment_sentiments_label"])
            .size()
            .reset_index(name="count")
        )
        fig_comment = px.bar(
            comment_df, x="domain", y="count", color="comment_sentiments_label",
            title="💬 Comment Sentiment by Domain",
            color_discrete_map={"Positive": "#5CFFB4", "Neutral": "#BBB", "Negative": "#F66"},
        )
        st.plotly_chart(fig_comment, use_container_width=True)

# --- NewsAPI-Only Visuals ---
if platform == "NewsAPI":
    if "source" in df.columns:
        source_counts = df["source"].value_counts().head(15)
        st.markdown("🗞️ <strong>Top News Sources</strong>", unsafe_allow_html=True)
        st.bar_chart(source_counts)

    if "sentiment_score" in df.columns:
        sentiment_by_source = (
            df.groupby("source")["sentiment_score"].mean().reset_index()
        ).head(20)
        fig_source_sentiment = px.bar(
            sentiment_by_source, x="source", y="sentiment_score",
            title="🧠 Avg Sentiment by News Source", color="source",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_source_sentiment, use_container_width=True)

combined_df = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "Combined_Data.csv")

def find_cat(data):
    if data['source'] == 'reddit':
        return "Reddit"
    else:
        return "News"

combined_df['category'] = combined_df.apply(find_cat,axis = 1)
compare_df = (
    combined_df.groupby(["domain", "sentiment_label", "category"])
    .size().reset_index(name="count")
)

fig_compare = px.bar(
    compare_df, x="domain", y="count", color="category",
    facet_col="sentiment_label", title="🧭 Sentiment Comparison: Reddit vs News"
)
st.plotly_chart(fig_compare, use_container_width=True)