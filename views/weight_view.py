from datetime import date
from models.weight import log_weight, get_weight_log, get_weight_change


def prompt_log_weight():
    today = date.today().isoformat()
    date_input = input(f"  Date [{today}]: ").strip() or today

    try:
        kg = float(input("  Weight (kg): ").strip())
    except ValueError:
        print("  Invalid number, not saved.\n")
        return

    notes = input("  Notes (optional): ").strip()
    log_weight(date_input, kg, notes)
    print(f"\n  ✅  Logged {kg} kg on {date_input}\n")


def show_weight_log():
    rows = get_weight_log(limit=30)
    if not rows:
        print("\n  No weight entries yet.\n")
        return

    change_7  = get_weight_change(7)
    change_30 = get_weight_change(30)

    print(f"\n  {'Date':<14} {'Weight (kg)':<14} Notes")
    print("  " + "─" * 45)
    for r in rows:
        print(f"  {r['date']:<14} {r['weight_kg']:<14} {r['notes'] or ''}")

    print()
    if change_7 is not None:
        arrow = "▲" if change_7 > 0 else "▼" if change_7 < 0 else "─"
        print(f"  7-day change:  {arrow} {abs(change_7):.2f} kg")
    if change_30 is not None:
        arrow = "▲" if change_30 > 0 else "▼" if change_30 < 0 else "─"
        print(f"  30-day change: {arrow} {abs(change_30):.2f} kg")
    print()
