import psycopg2
import random

# Sample messages to pick from
sample_texts = [
    "I love this scene!",
    "Wow, that was unexpected!",
    "This part is boring...",
    "Amazing visuals!",
    "Not sure about this...",
    "Hilarious!",
    "So emotional...",
    "I like this character!",
    "Interesting plot twist!"
]

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Project1_VidMood",
    user="postgres",
    password="Prathi27*",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Fetch all scenes
cur.execute("SELECT scene_id, start_time, end_time FROM scenes")
scenes = cur.fetchall()

# For each scene, generate 1-5 random chat messages
for scene_id, start_time, end_time in scenes:
    num_messages = random.randint(1, 5)
    for _ in range(num_messages):
        video_time = round(random.uniform(start_time, end_time), 2)
        message_text = random.choice(sample_texts)
        cur.execute("""
            INSERT INTO chat_messages (video_time_seconds, message_text)
            VALUES (%s, %s)
        """, (video_time, message_text))

conn.commit()
cur.close()
conn.close()

print(f"Generated sample chat messages for {len(scenes)} scenes!")
