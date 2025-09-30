import psycopg2
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# nltk.download('vader_lexicon')

# Initialize the analyzer
sia = SentimentIntensityAnalyzer()

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Project1_VidMood",
    user="postgres",
    password="Prathi27*",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Fetch all chat messages
cur.execute("SELECT message_id, message_text FROM chat_messages")
chat_rows = cur.fetchall()

# Analyze and insert sentiment only if not already inserted
for message_id, message in chat_rows:
    # Check if sentiment already exists for this chat_id
    cur.execute("SELECT 1 FROM chat_sentiment WHERE message_id = %s", (message_id,))
    if cur.fetchone():
        continue  # already inserted, skip

    score = sia.polarity_scores(message)['compound']
    if score >= 0.05:
        label = 'positive'
    elif score <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    cur.execute("""
        INSERT INTO chat_sentiment (message_id, sentiment_label, sentiment_score)
        VALUES (%s, %s, %s)
    """, (message_id, label, score))

conn.commit()
cur.close()
conn.close()

print(f"Sentiment analysis completed for {len(chat_rows)} messages!")
