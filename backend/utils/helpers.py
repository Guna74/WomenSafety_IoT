import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "safety.db")

def save_to_db(data, risk):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO data (heart_rate, temperature, motion, risk, lat, lon)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["heart_rate"],
        data["temperature"],
        data["motion"],
        risk,
        data.get("lat"),
        data.get("lon")
    ))

    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT heart_rate, temperature, motion, risk, timestamp FROM data ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()

    return [{"heart_rate": r[0], "temperature": r[1], "motion": r[2], "risk": r[3], "timestamp": f"{r[4]}Z"} for r in rows]

def get_aggregated_history(period="hours"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if period == "hours":
        sql = "SELECT strftime('%Y-%m-%d %H:00', timestamp, '+5 hours', '+30 minutes') as time_group, AVG(heart_rate), AVG(motion) FROM data GROUP BY time_group ORDER BY time_group DESC LIMIT 24"
    elif period == "days":
        sql = "SELECT strftime('%Y-%m-%d', timestamp, '+5 hours', '+30 minutes') as time_group, AVG(heart_rate), AVG(motion) FROM data GROUP BY time_group ORDER BY time_group DESC LIMIT 30"
    elif period == "weeks":
        sql = "SELECT strftime('%Y-%W', timestamp, '+5 hours', '+30 minutes') as time_group, AVG(heart_rate), AVG(motion) FROM data GROUP BY time_group ORDER BY time_group DESC LIMIT 12"
    else:
        conn.close()
        return []

    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    
    # Reverse to return oldest first for charts natively
    result = [{"time": r[0], "heart_rate": round(r[1], 1), "motion": round(r[2], 1)} for r in rows]
    return list(reversed(result))

def get_latest_state():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT heart_rate, temperature, motion, risk, lat, lon FROM data ORDER BY rowid DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()

    if row is None:
        return {
            "heart_rate": 0,
            "temperature": 0,
            "motion": 0,
            "risk": "SAFE",
            "lat": 0,
            "lon": 0
        }

    return {
        "heart_rate": row[0],
        "temperature": row[1],
        "motion": row[2],
        "risk": row[3],
        "lat": row[4],
        "lon": row[5]
    }