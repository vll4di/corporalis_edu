from db import get_connection


def check_and_update_pr(exercise_name: str, weight_kg: float, reps: int, date: str):
    """Update the PR for an exercise if this set beats the current record."""
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM personal_records WHERE exercise_name = ?", (exercise_name,)
        ).fetchone()

        if existing is None or weight_kg > existing["weight_kg"]:
            conn.execute(
                """
                INSERT INTO personal_records (exercise_name, weight_kg, reps, date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(exercise_name) DO UPDATE SET
                    weight_kg = excluded.weight_kg,
                    reps      = excluded.reps,
                    date      = excluded.date
                """,
                (exercise_name, weight_kg, reps, date),
            )
            return True  # new PR hit
    return False


def get_all_prs():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM personal_records ORDER BY exercise_name"
        ).fetchall()
