import sys
import sqlite3
from collections import defaultdict
from .audio import get_constellation_map
from .fingerprint import generate_fingerprints
from .config import DB_PATH, MIN_MATCHES

def identify(query_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("Extracting query fingerprints (first 15 seconds)...")
    constellation = get_constellation_map(query_path, limit_duration=15)
    print(f"Found {len(constellation)} peaks")
    
    q_fps = generate_fingerprints(constellation)
    print(f"Generated {len(q_fps)} fingerprints")
    
    if len(q_fps) == 0:
        print("❌ No fingerprints generated from query")
        conn.close()
        return
    
    # Batch database query
    hash_list = [h for h, _ in q_fps]
    placeholders = ','.join('?' * len(hash_list))
    
    print("Querying database...")
    c.execute(f"SELECT hash, song, offset FROM fingerprints WHERE hash IN ({placeholders})", hash_list)
    all_matches = c.fetchall()
    
    print(f"Found {len(all_matches)} hash matches")
    
    if len(all_matches) == 0:
        print("❌ No matches found in database")
        conn.close()
        return
    
    # Build hash -> query_offset mapping
    hash_to_offset = {h: off for h, off in q_fps}
    
    # Count matches at each offset for each song
    offset_histogram = defaultdict(lambda: defaultdict(int))
    
    for match_hash, song, db_offset in all_matches:
        q_offset = hash_to_offset[match_hash]
        time_delta = int(db_offset) - q_offset
        offset_histogram[song][time_delta] += 1
    
    # Score each song by its best aligned offset
    results = []
    for song, deltas in offset_histogram.items():
        best_delta = max(deltas, key=deltas.get)
        score = deltas[best_delta]
        total = sum(deltas.values())
        results.append((song, score, best_delta, total))
    
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n🎵 Top 10 Results:")
    for i, (song, score, delta, total) in enumerate(results[:10], 1):
        print(f"{i:2d}. {song}")
        print(f"     Score: {score} | Total matches: {total} | Time offset: {delta} frames")
    
    if results and results[0][1] >= MIN_MATCHES:
        print(f"\n✅ MATCH: {results[0][0]}")
        print(f"   Confidence: {results[0][1]} aligned matches at offset {results[0][2]}")
        return {"song": results[0][0], "score": results[0][1]}
    else:
        print("\n❌ No confident match found")
        return None
    
    conn.close()

# def identify(path):
#     constellation = get_constellation_map(path, limit_duration=15)
#     q_fps = generate_fingerprints(constellation)

#     if not q_fps:
#         return None

#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     hashes = [h for h, _ in q_fps]
#     placeholders = ",".join("?" * len(hashes))

#     c.execute(f"""
#         SELECT hash, song, offset
#         FROM fingerprints
#         WHERE hash IN ({placeholders})
#     """, hashes)

#     matches = c.fetchall()
#     conn.close()

#     histogram = defaultdict(lambda: defaultdict(int))
#     q_map = dict(q_fps)

#     for h, song, db_offset in matches:
#         delta = db_offset - q_map[h]
#         histogram[song][delta] += 1

#     best = None
#     best_score = 0

#     for song, offsets in histogram.items():
#         score = max(offsets.values())
#         print(song,score)
#         if score > best_score:
#             best_score = score
#             best = song
#     if best_score >= MIN_MATCHES:
#         return {"song": best, "score": best_score}

#     return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.matcher <query_audio>")
        sys.exit(1)

    query_path = sys.argv[1]
    result = identify(query_path)
    print(result)
