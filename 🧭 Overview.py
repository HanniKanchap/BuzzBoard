import streamlit as st
import urllib.parse 
# Page configuration
st.set_page_config(
    page_title="BuzzBoard Home",
    page_icon="🧠",
    layout="wide"
)

with st.sidebar:
    st.markdown("""
    ### 👋 Welcome to BuzzBoard
    Visualize public sentiment across Reddit & News. 

    - 🧠 Track emotions 
    -  📊 Compare platforms
    - 📡 Decode the discourse
    """)

st.markdown("""
<style>
.buzz-container {
    background-color: #29263A;
    border: 2px solid #444;
    border-radius: 14px;
    box-shadow: 0 0 14px rgba(240, 240, 240, 0.12);
    padding: 38px;
    text-align: center;
    margin-bottom: 32px;
}
.buzz-title {
    font-size: 54px;
    font-style : Sans-sherif;
    color: #FFF6F9;
    font-weight: 800;
    letter-spacing: 2px;
    text-shadow: 0 0 4px grey;
    margin-bottom: 8px;
}
.buzz-subtitle {
    font-size: 18px;
    color: #DADADA;
    font-family : Arial;
    font-weight: 400;
    text-shadow: 0 0 1.5px white;
    letter-spacing: 0.6px;
}
</style>

<div class='buzz-container'>
    <div class='buzz-title'> BuzzBoard </div>
    <div class='buzz-subtitle'>Track emotion. Compare narrative. Reveal impact. </div>
</div>
""", unsafe_allow_html=True)

st.image('./assets/Hero_Banner.jpeg', caption='BuzzBoard · Emotional Pulse Dashboard', use_container_width=True)
# 📊 Snapshot Metrics

st.subheader("📊 System Snapshot")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Domains Tracked", "20")
col2.metric("Sources Connected", "2")
col3.metric("Records Processed", "1000+")
col4.metric("Live Fetch Status" , "Available")


# 🚀 BuzzBoard Capabilities Section
st.subheader("🚀 BuzzBoard Capabilities")

st.markdown("""
<style>
.feature-box {
    background-color: #3A3440;
    border: 1px solid grey;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 0 6px rgba(249, 168, 201, 0.15);
}
.feature-title {
    font-size: 18px;
    color: #FFF6F9;
    font-weight: 600;
    margin-bottom: 6px;
}
.feature-desc {
    font-size: 14px;
    color: #E0E0E0;
    line-height: 1.5;
}
</style>

<div class='feature-box'>
    <div class='feature-title'>🧠 Sentiment Analysis</div>
    <div class='feature-desc'>Explore emotional tone across Reddit posts and news headlines using AI-powered classifiers.</div>
</div>

<div class='feature-box'>
    <div class='feature-title'>📡 Domain Buzz Tracking</div>
    <div class='feature-desc'>Monitor engagement levels and topic intensity across innovation domains in near real-time.</div>
</div>

<div class='feature-box'>
    <div class='feature-title'>📊 Unified Dashboard</div>
    <div class='feature-desc'>Compare Reddit vs NewsAPI sentiment, visualize trends, and filter by source, time, or emotion.</div>
</div>

<div class='feature-box'>
    <div class='feature-title'>🛰️ Live Data Fetching</div>
    <div class='feature-desc'>Pull fresh data instantly from chosen domains, cleaned and formatted through modular pipelines.</div>
</div><br><br>
""", unsafe_allow_html=True)

# ❓ FAQ Section
st.subheader("💡 Frequently Asked Questions")
with st.expander(" What does BuzzBoard do?"):
    st.write("""
BuzzBoard is a sentiment intelligence platform that analyzes emotional trends across Reddit and news sources.  
It helps users visualize how people feel about key themes like politics, technology, climate, and more — using charts, comparisons, and emotional signal tracking.
""")

with st.expander("What sources does BuzzBoard use?"):
    st.write("BuzzBoard gathers data from Reddit (public posts + comments) and NewsAPI (news articles across publishers).")

with st.expander("How are sentiment labels assigned?"):
    st.write("Each entry is processed using transformer-based sentiment classifiers to assign 'Positive', 'Neutral', or 'Negative' labels.")

with st.expander("Can I fetch live data or use cached results?"):
    st.write("Yes! In the 'Live Fetch' page, you can select domains and choose between real-time scraping or using stored cleaned datasets.")

with st.expander("What does 'engagement score' represent?"):
    st.write("It reflects audience interaction — comment volume, upvotes, and post reach — with tiers like 'High', 'Medium', and 'Low'.")

##  Feedback 

st.markdown("---")
st.markdown("### 💌 Contact Us")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    query = st.text_area("Your Message", height=150)
    submitted = st.form_submit_button("📨 Create Email")

    if submitted:
        if name and user_email and query:
            subject = urllib.parse.quote("BuzzBoard Inquiry / Suggestion")
            body = urllib.parse.quote(f"Name: {name}\nEmail: {user_email}\n\nMessage:\n{query}")
            mailto_link = f"mailto:hannikanchap11@gmail.com?subject={subject}&body={body}"

            st.markdown(f"""<p style="text-decoration:none;">
            👉 <a href="{mailto_link}" style = 'text-decoration:white; color:white;'>Click here to open your email client and send</a></p>""", unsafe_allow_html=True)   
            st.info("✅ Your message has been pre-filled. Just hit send from your mail app.")
        else:
            st.warning("⚠️ Please complete all fields before submitting.")


# 🛠 Footer
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size: 13px; color: #999;'>
BuzzBoard v1.0 | Developed by HANNI | Streamlit-powered | Data from Reddit + NewsAPI
</p>
""", unsafe_allow_html=True)