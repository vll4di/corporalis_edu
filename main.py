import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from db import init_db
from views.workout_view      import prompt_log_workout, show_workout_history
from views.measurements_view import prompt_log_measurement, show_measurements
from views.stats_view        import show_personal_records
from views.calorie_view      import prompt_log_food, show_daily_summary, prompt_set_goal
from views.weight_view       import prompt_log_weight, show_weight_log

MENU = """
╔══════════════════════════════════════╗
║           GYM TRACKER                ║
╠══════════════════════════════════════╣
║  WORKOUTS                            ║
║   1. Log workout                     ║
║   2. View workout history            ║
║   3. View personal records           ║
╠══════════════════════════════════════╣
║  NUTRITION                           ║
║   4. Log food (Open Food Facts)      ║
║   5. View today's calories           ║
║   6. Set calorie / macro goal        ║
╠══════════════════════════════════════╣
║  BODY                                ║
║   7. Log weight                      ║
║   8. View weight log                 ║
║   9. Log body measurements           ║
║   0. View body measurements          ║
╠══════════════════════════════════════╣
║   q. Quit                            ║
╚══════════════════════════════════════╝
"""


def main():
    init_db()
    while True:
        print(MENU)
        choice = input("Choice: ").strip().lower()

        if   choice == "1": prompt_log_workout()
        elif choice == "2": show_workout_history()
        elif choice == "3": show_personal_records()
        elif choice == "4": prompt_log_food()
        elif choice == "5": show_daily_summary()
        elif choice == "6": prompt_set_goal()
        elif choice == "7": prompt_log_weight()
        elif choice == "8": show_weight_log()
        elif choice == "9": prompt_log_measurement()
        elif choice == "0": show_measurements()
        elif choice in ("q", "quit", "exit"):
            print("\nSee you next session 💪\n")
            break
        else:
            print("\n  Unrecognised option, try again.\n")


if __name__ == "__main__":
    main()
