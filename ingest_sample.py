import psycopg2
from datetime import datetime

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="Project1_VidMood",        # database name you created
    user="postgres",         # your DB user
    password="Prathi27*",# your DB password
    host="localhost",
    port=5432
)

cur = conn.cursor()

# Insert a sample video
cur.execute("""
INSERT INTO videos (title, duration_seconds)
VALUES (%s, %s) RETURNING video_id
""", ("Sample Video", 120.0))
video_id = cur.fetchone()[0]

# Insert a scene for this video
cur.execute("""
INSERT INTO scenes (video_id, scene_index, start_time, end_time)
VALUES (%s, %s, %s, %s)
""", (video_id, 1, 0.0, 30.0))

# Insert a sample chat message
cur.execute("""
INSERT INTO chat_messages (video_id, user_id, message_text, message_ts, video_time_seconds)
VALUES (%s, %s, %s, %s, %s)
""", (video_id, "user123", "This scene is great!", datetime.now(), 5.0))

conn.commit()
cur.close()
conn.close()

print("Sample data inserted successfully!")
