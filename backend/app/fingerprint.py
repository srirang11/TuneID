import hashlib
from .config import *


def generate_fingerprints(constellation):
    """
    Generate fingerprints from constellation map.
    Each fingerprint: hash of (freq1, freq2, time_delta) -> anchor_time
    """
    fingerprints = []
    
    for i in range(len(constellation)):
        anchor_time, anchor_freq = constellation[i]
        
        # Look for target points in the zone after this anchor
        target_zone_start = anchor_time + TARGET_ZONE_START
        target_zone_end = anchor_time + TARGET_ZONE_START + TARGET_ZONE_WIDTH
        
        targets_found = 0
        
        for j in range(i + 1, len(constellation)):
            target_time, target_freq = constellation[j]
            
            # Stop if we've gone past the target zone
            if target_time > target_zone_end:
                break
            
            # Skip if before target zone
            if target_time < target_zone_start:
                continue
            
            # Create fingerprint
            time_delta = target_time - anchor_time
            
            # Hash combines the two frequencies and their time relationship
            hash_input = f"{anchor_freq}|{target_freq}|{time_delta}"
            fp_hash = hashlib.sha1(hash_input.encode()).hexdigest()[:12]
            
            fingerprints.append((fp_hash, anchor_time))
            
            targets_found += 1
            if targets_found >= FAN_VALUE:
                break
    
    return fingerprints


# def generate_fingerprints(constellation):
#     fingerprints = []

#     for i in range(len(constellation)):
#         anchor_time, anchor_freq = constellation[i]

#         for j in range(i + 1, len(constellation)):
#             target_time, target_freq = constellation[j]

#             if target_time - anchor_time > TARGET_ZONE_WIDTH:
#                 break

#             if target_time <= anchor_time:
#                 continue

#             delta = target_time - anchor_time
#             raw = f"{anchor_freq}|{target_freq}|{delta}"
#             h = hashlib.sha1(raw.encode()).hexdigest()[:16]

#             fingerprints.append((h, anchor_time))
#             if len(fingerprints) >= FAN_VALUE:
#                 break

#     return fingerprints
