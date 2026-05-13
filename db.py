import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "gym.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS workouts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                date    TEXT NOT NULL,
                notes   TEXT
            );

            CREATE TABLE IF NOT EXISTS exercises (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
                name       TEXT NOT NULL,
                sets       INTEGER NOT NULL,
                reps       INTEGER NOT NULL,
                weight_kg  REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS measurements (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                date         TEXT NOT NULL,
                weight_kg    REAL,
                body_fat_pct REAL,
                notes        TEXT
            );

            CREATE TABLE IF NOT EXISTS personal_records (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL UNIQUE,
                weight_kg     REAL NOT NULL,
                reps          INTEGER NOT NULL,
                date          TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS calorie_goals (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                date         TEXT NOT NULL UNIQUE,
                calories     INTEGER NOT NULL,
                protein_g    REAL,
                carbs_g      REAL,
                fat_g        REAL
            );

            CREATE TABLE IF NOT EXISTS food_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                date         TEXT NOT NULL,
                meal         TEXT NOT NULL DEFAULT 'other',
                food_name    TEXT NOT NULL,
                brand        TEXT,
                quantity_g   REAL NOT NULL,
                calories     REAL NOT NULL,
                protein_g    REAL,
                carbs_g      REAL,
                fat_g        REAL
            );

            CREATE TABLE IF NOT EXISTS weight_log (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                date      TEXT NOT NULL UNIQUE,
                weight_kg REAL NOT NULL,
                notes     TEXT
            );
        """)
