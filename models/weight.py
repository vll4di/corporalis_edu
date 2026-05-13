from db import get_connection


def log_weight(date: str, weight_kg: float, notes: str = ""):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO weight_log (date, weight_kg, notes)
               VALUES (?, ?, ?)
               ON CONFLICT(date) DO UPDATE SET
                   weight_kg = excluded.weight_kg,
                   notes     = excluded.notes""",
            (date, weight_kg, notes),
        )


def get_weight_log(limit: int = 30):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM weight_log ORDER BY date DESC LIMIT ?", (limit,)
        ).fetchall()


def get_weight_change(days: int = 7) -> float | None:
    """Return kg change over the last N days (positive = gained, negative = lost)."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT weight_kg FROM weight_log ORDER BY date DESC LIMIT ?", (days,)
        ).fetchall()
    if len(rows) < 2:
        return None
    return round(rows[0]["weight_kg"] - rows[-1]["weight_kg"], 2)
