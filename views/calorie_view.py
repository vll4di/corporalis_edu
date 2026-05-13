from datetime import date
from api.food_search import search_food
from models.calories import (
    log_food, get_food_log, get_daily_totals,
    set_calorie_goal, get_calorie_goal, MEALS
)


def _bar(value, goal, width=20) -> str:
    if not goal or goal == 0:
        return ""
    filled = min(int((value / goal) * width), width)
    color = "over" if value > goal else "ok"
    bar = "█" * filled + "░" * (width - filled)
    suffix = " ⚠ over!" if value > goal else ""
    return f"[{bar}] {value:.0f}/{goal:.0f}{suffix}"


def prompt_log_food():
    today = date.today().isoformat()
    date_input = input(f"  Date [{today}]: ").strip() or today

    print("  Meals:", ", ".join(MEALS))
    meal = input("  Meal: ").strip().lower() or "other"
    if meal not in MEALS:
        meal = "other"

    query = input("  Search food (name or brand): ").strip()
    if not query:
        return

    print("  🔍 Searching Open Food Facts…")
    results = search_food(query)

    if not results:
        print("  No results found. Try a different search term.\n")
        return

    print()
    for i, r in enumerate(results):
        brand = f" ({r['brand']})" if r['brand'] else ""
        print(f"  {i+1}. {r['name']}{brand}")
        print(f"     {r['calories']:.0f} kcal | "
              f"P: {r['protein_g'] or '?'}g  C: {r['carbs_g'] or '?'}g  F: {r['fat_g'] or '?'}g  "
              f"(per 100g)")

    print()
    choice = input(f"  Select 1-{len(results)} (or Enter to cancel): ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(results)):
        print("  Cancelled.\n")
        return

    food = results[int(choice) - 1]

    try:
        qty = float(input(f"  Quantity (g) for {food['name']}: ").strip())
    except ValueError:
        print("  Invalid quantity, cancelled.\n")
        return

    log_food(
        date=date_input, meal=meal,
        food_name=food["name"], brand=food["brand"],
        quantity_g=qty,
        calories_per_100g=food["calories"],
        protein_per_100g=food["protein_g"],
        carbs_per_100g=food["carbs_g"],
        fat_per_100g=food["fat_g"],
    )

    scaled_kcal = food["calories"] * qty / 100
    print(f"\n  ✅  Logged {food['name']} ({qty:.0f}g) — {scaled_kcal:.0f} kcal\n")


def show_daily_summary():
    today = date.today().isoformat()
    date_input = input(f"  Date [{today}]: ").strip() or today

    rows   = get_food_log(date_input)
    totals = get_daily_totals(date_input)
    goal   = get_calorie_goal(date_input)

    if not rows:
        print(f"\n  Nothing logged for {date_input}.\n")
        return

    print(f"\n  ── Food log for {date_input} ──\n")
    current_meal = None
    for r in rows:
        if r["meal"] != current_meal:
            current_meal = r["meal"]
            print(f"  {current_meal.upper()}")
        brand = f" ({r['brand']})" if r["brand"] else ""
        print(f"    {r['food_name']}{brand}  {r['quantity_g']:.0f}g  "
              f"{r['calories']:.0f} kcal  "
              f"P:{r['protein_g'] or '—'}  C:{r['carbs_g'] or '—'}  F:{r['fat_g'] or '—'}")

    print()
    print(f"  TOTALS  Calories: {totals['calories'] or 0:.0f} kcal  "
          f"Protein: {totals['protein_g'] or 0:.0f}g  "
          f"Carbs: {totals['carbs_g'] or 0:.0f}g  "
          f"Fat: {totals['fat_g'] or 0:.0f}g")

    if goal:
        print()
        print(f"  GOAL    {_bar(totals['calories'] or 0, goal['calories'])}")
        if goal.get("protein_g"):
            print(f"  Protein {_bar(totals['protein_g'] or 0, goal['protein_g'])}")
        if goal.get("carbs_g"):
            print(f"  Carbs   {_bar(totals['carbs_g'] or 0, goal['carbs_g'])}")
        if goal.get("fat_g"):
            print(f"  Fat     {_bar(totals['fat_g'] or 0, goal['fat_g'])}")
    print()


def prompt_set_goal():
    today = date.today().isoformat()
    date_input = input(f"  Effective from [{today}]: ").strip() or today

    try:
        cal  = int(input("  Daily calorie goal (kcal): ").strip())
        pro  = input("  Protein goal g (Enter to skip): ").strip()
        carb = input("  Carbs goal g   (Enter to skip): ").strip()
        fat  = input("  Fat goal g     (Enter to skip): ").strip()
    except ValueError:
        print("  Invalid input, goal not saved.\n")
        return

    set_calorie_goal(
        date_input, cal,
        float(pro)  if pro  else None,
        float(carb) if carb else None,
        float(fat)  if fat  else None,
    )
    print(f"\n  ✅  Goal saved: {cal} kcal from {date_input}\n")
