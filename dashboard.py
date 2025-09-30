import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Project1_VidMood",
    user="postgres",
    password="Prathi27*",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Fetch scene-level sentiment aggregation
cur.execute("""
    SELECT s.scene_id,
           s.start_time,
           s.end_time,
           COUNT(cm.message_id) AS total_messages,
           SUM(CASE WHEN cs.sentiment_label='positive' THEN 1 ELSE 0 END) AS positive,
           SUM(CASE WHEN cs.sentiment_label='neutral' THEN 1 ELSE 0 END) AS neutral,
           SUM(CASE WHEN cs.sentiment_label='negative' THEN 1 ELSE 0 END) AS negative,
           AVG(cs.sentiment_score) AS avg_score
    FROM scenes s
    LEFT JOIN chat_messages cm ON cm.video_time_seconds >= s.start_time
                              AND cm.video_time_seconds <= s.end_time
    LEFT JOIN chat_sentiment cs ON cs.message_id = cm.message_id
    GROUP BY s.scene_id, s.start_time, s.end_time
    ORDER BY s.scene_id
""")

rows = cur.fetchall()
cur.close()
conn.close()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=[
    "scene_id", "start_time", "end_time", "total_messages", "positive", "neutral", "negative", "avg_score"
])

st.title("Video Mood Analytics Dashboard")

st.subheader("Scene-by-Scene Sentiment Overview")
st.dataframe(df)

# Plot stacked bar chart of sentiment counts per scene
fig = px.bar(df,
             x="scene_id",
             y=["positive", "neutral", "negative"],
             title="Sentiment Distribution per Scene",
             labels={"value":"Message Count", "scene_id":"Scene ID"},
             text_auto=True)
st.plotly_chart(fig)

# Plot average sentiment score
fig2 = px.line(df, x="scene_id", y="avg_score", title="Average Sentiment Score per Scene",
               labels={"avg_score":"Avg Sentiment", "scene_id":"Scene ID"})
st.plotly_chart(fig2)
