import urllib.request
import urllib.parse
import json

BASE_URL = "https://world.openfoodfacts.org"
FIELDS   = "product_name,brands,nutriments,serving_size,quantity"


def search_food(query: str, page_size: int = 5) -> list[dict]:
    """Full-text search via Open Food Facts v1 API. Returns a simplified list."""
    params = urllib.parse.urlencode({
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": page_size,
        "fields": FIELDS,
    })
    url = f"{BASE_URL}/cgi/search.pl?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": "GymTrackerCLI/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠  API error: {e}")
        return []

    results = []
    for p in data.get("products", []):
        n = p.get("nutriments", {})
        results.append({
            "name":       p.get("product_name", "Unknown"),
            "brand":      p.get("brands", ""),
            "calories":   n.get("energy-kcal_100g") or n.get("energy-kcal"),
            "protein_g":  n.get("proteins_100g"),
            "carbs_g":    n.get("carbohydrates_100g"),
            "fat_g":      n.get("fat_100g"),
        })
    # filter out entries without calorie data
    return [r for r in results if r["calories"] is not None]
