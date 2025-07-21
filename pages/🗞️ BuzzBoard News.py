import streamlit as st
import pandas as pd
import numpy as np
from pipeline.news_pipeline import news_df_finalize
from pipeline.Clean_LiveData import clean_NewsAPIData         
from pathlib import Path

# -- Page Config --
st.set_page_config(page_title="News Insights", page_icon="🗞️", layout="wide")

# -- Header --
st.markdown("## 🗞️ BuzzBoard News Explorer")
st.markdown("Select a domain and data mode to view emotional signals from live and cached news articles.")

# -- Controls --
col1, col2 = st.columns(2)

domains = [
    "Technology", "Healthcare", "Climate", "Politics", "Economy", "Education", "Space",
    "Defense", "Media", "Privacy", "Law", "Social Movements", "Transportation", "Food",
    "Entertainment", "Science", "Artificial Intelligence", "Workforce", "Mental Health", "Disasters"
]

with col1:
    selected_domain = st.selectbox("📚 Choose Domain", domains)

with col2:
    fetch_mode = st.radio("📡 Data Mode", ["Cached", "Live Fetch"], horizontal=True)

# -- Load Data --
if st.button("🚀 Load Signals"):
    with st.spinner("BuzzBoard scanning headlines... 🗞️"):
        if fetch_mode == "Cached":
            df_path = Path(__file__).resolve().parent.parent / "data" / "Cleaned_NewsData.csv"
            df = pd.read_csv(df_path)

        else:
            raw_df = news_df_finalize(selected_domain)
            df = clean_NewsAPIData(raw_df)

        # -- Filter by Domain --
        df_filtered = df[df["domain"] == selected_domain]
        df_filtered = df_filtered.sort_values("Date_Format", ascending=False)

        st.markdown(f"### 🔍 Showing Buzz for **{selected_domain}** | Mode: **{fetch_mode}**")

        # -- Styled Article Display --
        for _, row in df_filtered.iterrows():
            has_image = pd.notna(row.thumbnail) and row.thumbnail.strip() != "" and row.thumbnail not in ['NaN',np.nan,'None',None]

            content_block = f"""
            <h4 style='color:#F0F0F0; margin-bottom:6px;'>{row.title}</h4>
            <p style='font-size:14px; color:#CCC; margin:0;'>
                📰 <strong>Source:</strong> {row.source} &nbsp; 📅 <strong>Date:</strong> {row.Date_Format}<br>
                🧠 <strong>Sentiment:</strong> {row.sentiment_label} &nbsp;
            </p>
            <a href="{row.url}" target="_blank" style='color:#08FDD8; text-decoration:none;'>🔗 View Full Article</a>
            """

            if has_image:
                img_tag = f"<img src='{row.thumbnail}' style='width:200px; height:auto; border-radius:6px;' />"
                inner_layout = f"<div style='display:flex; gap:20px;'>{img_tag}<div style='flex:1;'>{content_block}</div></div>"
            else:
                inner_layout = f"<div>{content_block}</div>"

            st.markdown(f"""
            <div style='
                background-color:#2D2B39;
                padding:16px;
                margin-bottom:16px;
                border-radius:10px;
                box-shadow:0 0 8px rgba(160,160,160,0.1);
            '>
                {inner_layout}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<p style='font-size:14px; color:#999;'>✅ Total Articles Displayed: <strong>{df_filtered.shape[0]}</strong></p>", unsafe_allow_html=True)

else:
    st.info("Select a domain and mode, then click 'Load Signals' to view NewsAPI insights.")