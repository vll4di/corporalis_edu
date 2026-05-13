from models.records import get_all_prs


def show_personal_records():
    prs = get_all_prs()
    if not prs:
        print("\n  No personal records yet — log some workouts first!\n")
        return

    print(f"\n  {'Exercise':<22} {'Weight (kg)':<14} {'Reps':<8} Date")
    print("  " + "-" * 55)
    for pr in prs:
        print(f"  {pr['exercise_name']:<22} {pr['weight_kg']:<14} {pr['reps']:<8} {pr['date']}")
    print()
