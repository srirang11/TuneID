import sys
import os
import sqlite3
from .audio import get_constellation_map
from .fingerprint import generate_fingerprints
from .database import init_db
from .config import DB_PATH

def ingest(music_dir):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for file in os.listdir(music_dir):
        print("FOUND FILE:", file)

        if not file.lower().endswith((".wav", ".mp3", ".flac")):
            print("SKIPPING (not audio):", file)
            continue

        path = os.path.join(music_dir, file)
        print("PROCESSING:", path)

        constellation = get_constellation_map(path)
        print("PEAKS FOUND:", len(constellation))

        fps = generate_fingerprints(constellation)
        print("FINGERPRINTS GENERATED:", len(fps))

        c.executemany(
            "INSERT INTO fingerprints VALUES (?, ?, ?)",
            [(h, file, t) for h, t in fps]
        )
        conn.commit()

    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.ingest <music_directory>")
        sys.exit(1)

    music_dir = sys.argv[1]
    ingest(music_dir)