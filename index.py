# CORD-19 Data Explorer App
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import streamlit as st

# -------------------------------
# Part 1: Load and Explore Data
# -------------------------------

# Load metadata.csv (zipped or unzipped)
df = pd.read_csv('metadata.csv.zip', low_memory=False)

# Drop rows missing critical info
df_clean = df.dropna(subset=['title', 'abstract', 'publish_time']).copy()

# Convert publish_time to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Remove rows with invalid dates
df_clean = df_clean[df_clean['publish_time'].notna()].copy()

# Extract year
df_clean['year'] = df_clean['publish_time'].dt.year

# Create abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

# -------------------------------
# Part 2: Streamlit App Layout
# -------------------------------

st.set_page_config(page_title="CORD-19 Explorer", layout="wide")
st.title("📚 CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers from the CORD-19 dataset")

# Year range slider
year_range = st.slider("Select publication year range", 2019, 2022, (2020, 2021))
filtered = df_clean[df_clean['year'].between(year_range[0], year_range[1])]

# -------------------------------
# Part 3: Display Data & Charts
# -------------------------------

# Sample data
st.subheader("📄 Sample Papers")
st.dataframe(filtered[['title', 'journal', 'year']].head(10))

# Publications by year
st.subheader("📊 Publications Over Time")
year_counts = filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

# Top journals
st.subheader("🏛️ Top Publishing Journals")
top_journals = filtered['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Word cloud of titles
st.subheader("☁️ Word Cloud of Paper Titles")
titles = filtered['title'].dropna().str.lower().str.replace(r'[^\w\s]', '', regex=True)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(titles))
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Source distribution
st.subheader("📦 Distribution by Source")
source_counts = filtered['source_x'].value_counts().head(10)
st.bar_chart(source_counts)

# -------------------------------
# Part 4: Footer
# -------------------------------

st.markdown("---")
st.caption("Built by Purity • Powered by Streamlit and Pandas")
