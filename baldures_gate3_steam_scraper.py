import requests
import pandas as pd
import time

# Steam App ID for Baldur's Gate 3
APP_ID = "1086940"

# Output CSV path
OUTPUT = r"C:\Disertation\reviews\game reviews\Baldur's Gate 3.csv"

all_reviews = []
cursor = "*"
count = 0
MAX_REVIEWS = 10000  # Adjust if needed

print("⏳ Scraping Steam reviews for Baldur's Gate 3...")

while True:
    url = (
        f"https://store.steampowered.com/appreviews/{APP_ID}"
        "?json=1&filter=recent&language=english"
        "&day_range=9223372036854775807"
        "&review_type=all&purchase_type=all"
        f"&cursor={cursor.replace('+', '%2B')}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print("🚫 Error fetching data!")
        break

    data = response.json()
    reviews = data.get("reviews", [])

    if not reviews:
        print("⚠️ No more reviews returned.")
        break

    for r in reviews:
        all_reviews.append({
            "author": r["author"]["steamid"],
            "review": r["review"],
            "timestamp": r["timestamp_created"],
            "voted_up": r["voted_up"],
            "votes_up": r["votes_up"],
            "votes_funny": r["votes_funny"],
            "weighted_vote_score": r["weighted_vote_score"],
            "playtime_forever": r["author"]["playtime_forever"],
        })

    count += len(reviews)
    print(f"📥 Collected so far: {count}")

    if count >= MAX_REVIEWS:
        print("🎯 Reached limit. Stopping...")
        break

    cursor = data.get("cursor")

    if not cursor:
        break

    time.sleep(1)  # avoid rate limiting

print("\n💾 Saving reviews...")

df = pd.DataFrame(all_reviews)
df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print("🎉 DONE!")
print(f"📁 Saved to: {OUTPUT}")
print(f"📊 Total reviews collected: {len(df)}")
