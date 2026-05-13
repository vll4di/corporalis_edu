from db import get_connection


def log_measurement(date: str, weight_kg: float = None, body_fat_pct: float = None, notes: str = ""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO measurements (date, weight_kg, body_fat_pct, notes) VALUES (?, ?, ?, ?)",
            (date, weight_kg, body_fat_pct, notes),
        )


def get_measurements(limit: int = 10):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM measurements ORDER BY date DESC LIMIT ?", (limit,)
        ).fetchall()
