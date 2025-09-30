import json
with open("scenes.json", "r") as f:
    scenes = json.load(f)


import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="Project1_VidMood",
    user="postgres",
    password="Prathi27*",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Replace this with your actual video_id from the videos table
video_id = 1  # Example: first video inserted

# Insert scenes into DB
for scene in scenes:
    cur.execute("""
        INSERT INTO scenes (video_id, scene_index, start_time, end_time, start_timestamp, end_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        video_id,
        scene["scene_index"],
        scene["start_seconds"],
        scene["end_seconds"],
        scene["start_time"],
        scene["end_time"]
    ))

conn.commit()
cur.close()
conn.close()

print(f"{len(scenes)} scenes inserted into database for video_id {video_id}!")
