from db import get_connection


MEALS = ["breakfast", "lunch", "dinner", "snack", "other"]


def log_food(date: str, meal: str, food_name: str, brand: str,
             quantity_g: float, calories_per_100g: float,
             protein_per_100g: float = None, carbs_per_100g: float = None,
             fat_per_100g: float = None):
    """Log a food item, scaling nutrients from per-100g values to actual quantity."""
    scale = quantity_g / 100
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO food_log
               (date, meal, food_name, brand, quantity_g, calories, protein_g, carbs_g, fat_g)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                date, meal, food_name, brand, quantity_g,
                round(calories_per_100g * scale, 1),
                round(protein_per_100g  * scale, 1) if protein_per_100g  is not None else None,
                round(carbs_per_100g    * scale, 1) if carbs_per_100g    is not None else None,
                round(fat_per_100g      * scale, 1) if fat_per_100g      is not None else None,
            ),
        )


def get_food_log(date: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM food_log WHERE date = ? ORDER BY meal, id",
            (date,)
        ).fetchall()


def get_daily_totals(date: str) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            """SELECT
                   ROUND(SUM(calories),  1) AS calories,
                   ROUND(SUM(protein_g), 1) AS protein_g,
                   ROUND(SUM(carbs_g),   1) AS carbs_g,
                   ROUND(SUM(fat_g),     1) AS fat_g
               FROM food_log WHERE date = ?""",
            (date,)
        ).fetchone()
    return dict(row) if row else {}


def set_calorie_goal(date: str, calories: int,
                     protein_g: float = None, carbs_g: float = None, fat_g: float = None):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO calorie_goals (date, calories, protein_g, carbs_g, fat_g)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(date) DO UPDATE SET
                   calories  = excluded.calories,
                   protein_g = excluded.protein_g,
                   carbs_g   = excluded.carbs_g,
                   fat_g     = excluded.fat_g""",
            (date, calories, protein_g, carbs_g, fat_g),
        )


def get_calorie_goal(date: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM calorie_goals WHERE date <= ? ORDER BY date DESC LIMIT 1",
            (date,)
        ).fetchone()
    return dict(row) if row else None
