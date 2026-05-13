from datetime import date
from models.workout import log_workout, log_exercise, get_all_workouts, get_workout_exercises
from models.records import check_and_update_pr


def prompt_log_workout():
    today = date.today().isoformat()
    date_input = input(f"Date [{today}]: ").strip() or today
    notes = input("Notes (optional): ").strip()

    workout_id = log_workout(date_input, notes)
    print(f"\n  Workout started. Log your exercises (type 'done' to finish).\n")

    while True:
        name = input("  Exercise name: ").strip()
        if name.lower() == "done":
            break
        if not name:
            continue

        try:
            sets      = int(input(f"  {name} — sets: "))
            reps      = int(input(f"  {name} — reps per set: "))
            weight_kg = float(input(f"  {name} — weight (kg): "))
        except ValueError:
            print("  ⚠  Invalid number, skipping exercise.")
            continue

        log_exercise(workout_id, name, sets, reps, weight_kg)

        if check_and_update_pr(name, weight_kg, reps, date_input):
            print(f"  🏆  New PR on {name}!\n")
        else:
            print()

    print(f"\n✅  Workout saved (id={workout_id}).\n")


def show_workout_history():
    workouts = get_all_workouts()
    if not workouts:
        print("\n  No workouts logged yet.\n")
        return

    print(f"\n  {'ID':<5} {'Date':<14} Notes")
    print("  " + "-" * 40)
    for w in workouts:
        print(f"  {w['id']:<5} {w['date']:<14} {w['notes'] or ''}")

    print()
    choice = input("  Enter workout ID to view details (or Enter to go back): ").strip()
    if choice.isdigit():
        show_workout_detail(int(choice))


def show_workout_detail(workout_id: int):
    exercises = get_workout_exercises(workout_id)
    if not exercises:
        print("\n  No exercises found for that workout.\n")
        return

    print(f"\n  {'Exercise':<20} {'Sets':<6} {'Reps':<6} {'Weight (kg)'}")
    print("  " + "-" * 45)
    for e in exercises:
        print(f"  {e['name']:<20} {e['sets']:<6} {e['reps']:<6} {e['weight_kg']}")
    print()
