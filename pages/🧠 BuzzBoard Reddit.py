import streamlit as st
import pandas as pd
from pipeline.reddit_pipeline import run_reddit_pipeline
from pipeline.Clean_LiveData import clean_RedditData
from pathlib import Path
from DataPreprocessing.collecting_Data import get_subdomains


# Page config
st.set_page_config(page_title="Reddit Insights", page_icon="🐝", layout="wide")

# --- Header ---
st.markdown("## 🧠 BuzzBoard Reddit Explorer")
st.markdown("Select a domain and data mode to view real-time emotional intelligence in Reddit threads.")

# --- Controls ---
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

# --- Trigger Load ---
if st.button("🚀 Load Buzz"):
    with st.spinner("BuzzBoard scanning threads... 🐝"):
        if fetch_mode == "Cached":
            df_path = Path(__file__).resolve().parent.parent / "data" / "Cleaned_RedditData.csv"
            df = pd.read_csv(df_path)

        else:
            sd = get_subdomains(selected_domain)
            data = pd.DataFrame([])
            for subDomain in sd:
                raw_df = run_reddit_pipeline(subDomain,selected_domain,15)
                data = pd.concat((data,raw_df))

            df = clean_RedditData(data)
            

        # --- Filter ---
        
        df_filtered = df[df["domain"] == selected_domain]
        df_filtered = df_filtered.sort_values("Date_Format", ascending=False) 
        
        st.markdown(f"### 🔍 Showing Buzz for **{selected_domain}** | Mode: **{fetch_mode}**")
        
        # --- Styled Results Container ---
        for i, row in df_filtered.iterrows():
            has_image = pd.notna(row.thumbnail) and row.thumbnail.strip() != ""

            content_block = f"""
            <h4 style='color:#F0F0F0; margin-bottom:6px;'>{row.title}</h4>
            <p style='font-size:14px; color:#CCC; margin:0;'>
                📅 <strong>Date:</strong> {row.Date_Format} &nbsp; 🕒 <strong>Time:</strong> {row.Time_Format}<br>
                🧠 <strong>Sentiment:</strong> {row.sentiment_label} &nbsp; 🔥 <strong>Engagement:</strong> {row.engagement_score}
            </p>
            <a href="{row.url}" target="_blank" style='color:#08FDD8; text-decoration:none;'>🔗 View Full Post</a>
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

        st.markdown(f"<p style='font-size:14px; color:#999;'>✅ Total Records Displayed: <strong>{df_filtered.shape[0]}</strong></p>", unsafe_allow_html=True)

else:
    st.info("Select a domain and mode, then click 'Load Buzz' to view Reddit insights.")