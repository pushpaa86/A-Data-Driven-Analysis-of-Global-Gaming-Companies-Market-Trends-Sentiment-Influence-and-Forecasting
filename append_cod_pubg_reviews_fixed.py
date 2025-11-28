import os
import pandas as pd

# === Paths ===
reviews_folder = r"C:\Disertation\reviews\game reviews"
combined_reviews_file = r"C:\Disertation\reviews\combined_reviews_50_games_ordered.csv"
output_file = r"C:\Disertation\reviews\combined_reviews_50_games_final.csv"

# Games to add
games_to_add = ["call of duty", "pubg mobile"]

def normalize(name: str) -> str:
    return name.strip().lower().replace("_", " ")

print("🔄 Loading combined review dataset...")

# --- Load combined file safely ---
try:
    df_combined = pd.read_csv(combined_reviews_file, encoding="utf-8", on_bad_lines="skip", engine="python")
except Exception as e:
    print(f"⚠️ Default read failed, retrying with latin1 encoding...\nError: {e}")
    df_combined = pd.read_csv(combined_reviews_file, encoding="latin1", on_bad_lines="skip", engine="python")

# --- Force all column names to strings ---
df_combined.columns = df_combined.columns.map(str)

# --- Identify the Game_Name column ---
game_col = None
for col in df_combined.columns:
    if "game" in col.lower():
        game_col = col
        break
if not game_col:
    game_col = df_combined.columns[-1]  # assume last column
    print(f"⚠️ Could not detect 'Game_Name' column automatically. Assuming: {game_col}")

# --- Normalize names ---
df_combined[game_col] = df_combined[game_col].astype(str).str.strip().str.lower()

existing_games = set(df_combined[game_col].unique())
print(f"📊 Found {len(existing_games)} existing games in combined file.\n")

# --- Append missing reviews ---
added_files = []
for file in os.listdir(reviews_folder):
    if not file.endswith(".csv"):
        continue
    lower_file = file.lower()
    for g in games_to_add:
        if g.replace(" ", "_") in lower_file or g in lower_file:
            print(f"🧩 Found match for '{g.title()}' in {file}")
            try:
                df_new = pd.read_csv(os.path.join(reviews_folder, file), encoding="utf-8", on_bad_lines="skip", engine="python")
                df_new["Game_Name"] = g.title()
                added_files.append(df_new)
                print(f"✅ Added {len(df_new)} reviews from {file}")
            except Exception as e:
                print(f"⚠️ Skipped {file}: {e}")

# --- Combine and save ---
if added_files:
    df_final = pd.concat([df_combined] + added_files, ignore_index=True)
    df_final.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n💾 Updated combined file saved as: {output_file}")
    print(f"🎮 Total unique games now: {df_final['Game_Name'].nunique()}")
else:
    print("⚠️ No new reviews added — files may already exist or not found.")
