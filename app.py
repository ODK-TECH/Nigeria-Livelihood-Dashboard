# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------
# Load Data
# --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("DATA.csv")
    return df

df = load_data()

# --------------------
# Page Config
# --------------------
st.set_page_config(
    page_title="Nigeria Livelihood & COVID-19 Dashboard",
    layout="wide",
    page_icon="🇳🇬"
)

# --------------------
# Sidebar Narrative
# --------------------
st.sidebar.header("📖 Storyline")
st.sidebar.markdown("""
This dashboard presents insights from **29,408 respondents**
on **livelihood sources** and the **impact of COVID-19** in Nigeria.

- Most Nigerians rely on **informal income** sources.
- COVID-19 disrupted markets & customers, hitting daily earners hardest.
- Cash remains dominant, limiting resilience during crises.

**Goal:** Highlight where interventions (digital finance, microloans, skills training) can make the most impact.
""")

# --------------------
# Dashboard Title
# --------------------
st.markdown("<h1 style='text-align: center; color: #006400;'>🇳🇬 Nigeria Livelihood & COVID-19 Impact Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Telling the story with data</h4>", unsafe_allow_html=True)

# --------------------
# Executive Summary
# --------------------
st.markdown("## 📌 Executive Summary")
st.markdown("""
The data tells a clear story:

1. **Income Vulnerability**
   Most Nigerians earn a living from **informal sources** — small-scale farming, petty trading, and personal services dominate.
   This makes them vulnerable to shocks due to **unstable wages** and **lack of social protection**.

2. **COVID-19 Impact**
   Lockdowns and market closures drastically reduced customers and restricted movement.
   **Daily earners** were hit hardest, facing **immediate income loss**.

3. **Cash Dominance**
   The majority receive income in **cash**, with low mobile money and banking use.
   This limits savings, slows aid delivery, and reduces financial resilience.

4. **Path Forward**
   To strengthen livelihoods, Nigeria should:
   - Expand **digital financial access**
   - Offer **microloans** to restart small businesses
   - Provide **training** to improve crisis resilience

**Sample Size:** 29,408 respondents
""")

st.markdown("---")

# --------------------
# Main Sources of Income
# --------------------
st.subheader("Main Sources of Income")
income_counts = df["E10"].value_counts().reset_index()
income_counts.columns = ["Income Source", "Count"]
fig_income = px.bar(
    income_counts.head(10),
    x="Count",
    y="Income Source",
    orientation="h",
    color="Count",
    color_continuous_scale="Greens",
    title="Top 10 Income Sources in Nigeria",
    width=1000,
    height=700
)
fig_income.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Income Source",
    plot_bgcolor="white",
    font=dict(size=14)
)
st.plotly_chart(fig_income, use_container_width=True)

# --------------------
# COVID-19 Business Challenges
# --------------------
st.subheader("COVID-19 Business Challenges")
challenges = df["E13e"].value_counts().reset_index()
challenges.columns = ["Challenge", "Count"]
fig_challenges = px.bar(
    challenges.head(10),
    x="Count",
    y="Challenge",
    orientation="h",
    color="Count",
    color_continuous_scale="Oranges",
    title="Top 10 Challenges Faced During COVID-19",
    width=1000,
    height=700
)
fig_challenges.update_layout(
    xaxis_title="Number of Respondents",
    yaxis_title="Challenge",
    plot_bgcolor="white",
    font=dict(size=14)
)
st.plotly_chart(fig_challenges, use_container_width=True)

# --------------------
# Attitudes (E13f)
# --------------------
if "E13f" in df.columns:
    st.subheader("Attitudes towards Business Recovery")
    attitudes = df["E13f"].value_counts().reset_index()
    attitudes.columns = ["Attitude", "Count"]
    fig_attitudes = px.bar(
        attitudes,
        x="Count",
        y="Attitude",
        orientation="h",
        color="Count",
        color_continuous_scale="RdBu",
        title="Optimism vs Pessimism in Recovery",
        width=1000,
        height=700
    )
    fig_attitudes.update_layout(
        xaxis_title="Number of Respondents",
        yaxis_title="Attitude",
        plot_bgcolor="white",
        font=dict(size=14)
    )
    st.plotly_chart(fig_attitudes, use_container_width=True)

# --------------------
# Heatmap (Top 10 E10 vs Top 10 E13e)
# --------------------
if "E10" in df.columns and "E13e" in df.columns:
    st.subheader("Top 10 Income Sources vs Top 10 COVID-19 Challenges Heatmap")

    top_income = df["E10"].value_counts().head(10).index
    top_challenges = df["E13e"].value_counts().head(10).index

    df_filtered = df[df["E10"].isin(top_income) & df["E13e"].isin(top_challenges)]
    heatmap_data = pd.crosstab(df_filtered["E10"], df_filtered["E13e"])
    heatmap_data = heatmap_data.loc[top_income, top_challenges]

    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="COVID-19 Challenge", y="Income Source", color="Count"),
        aspect="auto",
        color_continuous_scale="YlGnBu",
        title="Top 10 Income Sources vs Top 10 COVID-19 Challenges",
        width=1000,
        height=800
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)
