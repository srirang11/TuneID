import sqlite3
from .config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("DROP TABLE IF EXISTS fingerprints")
    
    c.execute("""
        CREATE TABLE fingerprints (
            hash TEXT,
            song TEXT,
            offset INTEGER
        )
    """)
    
    c.execute("CREATE INDEX idx_hash ON fingerprints(hash)")
    conn.commit()
    conn.close()


# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS fingerprints (
#             hash TEXT,
#             song TEXT,
#             offset INTEGER
#         )
#     """)
#     c.execute("CREATE INDEX IF NOT EXISTS idx_hash ON fingerprints(hash)")
#     conn.commit()
#     conn.close()
