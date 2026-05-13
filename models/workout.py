from db import get_connection


def log_workout(date: str, notes: str = "") -> int:
    """Insert a new workout and return its id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO workouts (date, notes) VALUES (?, ?)", (date, notes)
        )
        return cursor.lastrowid


def log_exercise(workout_id: int, name: str, sets: int, reps: int, weight_kg: float):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO exercises (workout_id, name, sets, reps, weight_kg) "
            "VALUES (?, ?, ?, ?, ?)",
            (workout_id, name, sets, reps, weight_kg),
        )


def get_all_workouts():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM workouts ORDER BY date DESC"
        ).fetchall()


def get_workout_exercises(workout_id: int):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM exercises WHERE workout_id = ?", (workout_id,)
        ).fetchall()
