from datetime import date
from models.measurements import log_measurement, get_measurements


def prompt_log_measurement():
    today = date.today().isoformat()
    date_input = input(f"Date [{today}]: ").strip() or today

    try:
        weight_kg    = input("  Body weight (kg, or Enter to skip): ").strip()
        weight_kg    = float(weight_kg) if weight_kg else None
        body_fat_pct = input("  Body fat % (or Enter to skip): ").strip()
        body_fat_pct = float(body_fat_pct) if body_fat_pct else None
    except ValueError:
        print("  ⚠  Invalid number, measurement not saved.")
        return

    notes = input("  Notes (optional): ").strip()
    log_measurement(date_input, weight_kg, body_fat_pct, notes)
    print("\n✅  Measurement saved.\n")


def show_measurements():
    rows = get_measurements(limit=15)
    if not rows:
        print("\n  No measurements logged yet.\n")
        return

    print(f"\n  {'Date':<14} {'Weight (kg)':<14} {'Body Fat %':<12} Notes")
    print("  " + "-" * 55)
    for r in rows:
        wt  = f"{r['weight_kg']:.1f}"    if r['weight_kg']    is not None else "—"
        bf  = f"{r['body_fat_pct']:.1f}" if r['body_fat_pct'] is not None else "—"
        print(f"  {r['date']:<14} {wt:<14} {bf:<12} {r['notes'] or ''}")
    print()
