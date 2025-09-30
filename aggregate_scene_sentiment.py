import psycopg2

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
cur.execute("""
    SELECT scene_id, start_time, end_time
    FROM scenes
""")
scenes = cur.fetchall()

# Prepare result storage
scene_sentiment_summary = []

# Process each scene
for scene_id, start_time, end_time in scenes:
    # Get all chat messages that fall within this scene
    cur.execute("""
        SELECT cs.sentiment_label, cs.sentiment_score
        FROM chat_sentiment cs
        JOIN chat_messages cm ON cs.message_id = cm.message_id
        WHERE cm.video_time_seconds >= %s AND cm.video_time_seconds <= %s
    """, (start_time, end_time))

    rows = cur.fetchall()

    if not rows:
        # No chat messages for this scene
        scene_sentiment_summary.append({
            "scene_id": scene_id,
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "avg_score": None
        })
        continue

    # Aggregate counts and average
    pos = sum(1 for r in rows if r[0] == "positive")
    neu = sum(1 for r in rows if r[0] == "neutral")
    neg = sum(1 for r in rows if r[0] == "negative")
    avg_score = sum(r[1] for r in rows) / len(rows)

    scene_sentiment_summary.append({
        "scene_id": scene_id,
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "avg_score": avg_score
    })

# Print summary
for summary in scene_sentiment_summary:
    print(summary)

cur.close()
conn.close()
