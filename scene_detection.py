import cv2
import os
import numpy as np

# ----------------------------
# Settings
# ----------------------------
video_path = r"D:\Projects\User_Retention\sample_video.mp4"
scene_threshold = 0.5      # Histogram difference threshold (0-1)
min_scene_len_sec = 3       # Minimum scene length in seconds
frame_skip = 5              # Analyze every 5th frame to speed up long videos
save_thumbnails = True
thumbnail_dir = "scene_thumbnails"

# Create thumbnail folder
if save_thumbnails and not os.path.exists(thumbnail_dir):
    os.makedirs(thumbnail_dir)

# ----------------------------
# Open video
# ----------------------------
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_sec = total_frames / fps
print(f"Video FPS: {fps}, Total frames: {total_frames}, Duration: {duration_sec:.2f}s")

prev_hist = None
frame_number = 0
scene_changes = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Skip frames for efficiency
    if frame_number % frame_skip != 0:
        frame_number += 1
        continue

    # Convert to HSV for color histogram
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8],
                        [0, 180, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()

    if prev_hist is not None:
        diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
        # If difference exceeds threshold and min_scene_len passed
        if diff > scene_threshold:
            if len(scene_changes) == 0 or (frame_number - scene_changes[-1]) >= min_scene_len_sec * fps:
                scene_changes.append(frame_number)
                if save_thumbnails:
                    thumb_path = os.path.join(thumbnail_dir, f"scene_{len(scene_changes)}.jpg")
                    cv2.imwrite(thumb_path, frame)

    prev_hist = hist
    frame_number += 1

cap.release()
# Add last frame as final scene
scene_changes.append(total_frames - 1)

# ----------------------------
# Convert frames to timestamps
# ----------------------------
def frame_to_time(frame, fps):
    seconds = frame / fps
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02}:{mins:02}:{secs:02}", round(seconds, 2)

# Pair scene boundaries
scenes = []
for i in range(len(scene_changes) - 1):
    start_frame = scene_changes[i]
    end_frame = scene_changes[i + 1]

    start_ts, start_sec = frame_to_time(start_frame, fps)
    end_ts, end_sec = frame_to_time(end_frame, fps)

    scenes.append({
        "scene_index": i + 1,
        "start_time": start_ts,
        "end_time": end_ts,
        "start_seconds": start_sec,
        "end_seconds": end_sec
    })

# ----------------------------
# Print results
# ----------------------------
print("\nDetected Scenes:")
for scene in scenes:
    print(f"Scene {scene['scene_index']}: {scene['start_time']} ({scene['start_seconds']}s) → "
          f"{scene['end_time']} ({scene['end_seconds']}s)")

import json

with open("scenes.json", "w") as f:
    json.dump(scenes, f)
