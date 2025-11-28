import requests
import pandas as pd
import time

APP_ID = 1245620     # Elden Ring Steam App ID
GAME_NAME = "Elden Ring"
OUTPUT = r"C:\Disertation\reviews\game reviews\Elden Ring.csv"

print(f"⏳ Scraping Steam reviews for {GAME_NAME} ...")

all_reviews = []
cursor = "*"
page = 1
MAX_REVIEWS = 10000   # adjust if needed

while len(all_reviews) < MAX_REVIEWS:
    print(f"🔍 Fetching page {page} ... total collected: {len(all_reviews)}")

    url = (
        f"https://store.steampowered.com/appreviews/{APP_ID}"
        "?json=1&language=english&filter=recent&day_range=9223372036854775807"
        f"&cursor={cursor}"
    )

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if "reviews" not in data or len(data["reviews"]) == 0:
            print("⚠️ No more reviews found.")
            break

        for rev in data["reviews"]:
            all_reviews.append({
                "recommend": rev.get("voted_up", ""),
                "review": rev.get("review", ""),
                "author_id": rev.get("author", {}).get("steamid", ""),
                "hours_played": rev.get("author", {}).get("playtime_forever", ""),
                "timestamp": rev.get("timestamp_created", ""),
            })

        cursor = data.get("cursor", "")
        page += 1
        time.sleep(1)

    except Exception as e:
        print("❌ Error:", e)
        break

print(f"\n📊 Total reviews collected: {len(all_reviews)}")

# Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print("\n✅ DONE! Saved at:")
print(OUTPUT)
