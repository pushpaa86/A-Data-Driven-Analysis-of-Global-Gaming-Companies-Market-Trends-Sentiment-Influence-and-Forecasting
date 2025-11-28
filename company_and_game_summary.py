import pandas as pd, numpy as np, os

# Paths (adjust if needed)
DOM_FILE = r"C:\Disertation\processed\FINAL_with_Dominance_MONTHLY.csv"
META_FILE = r"C:\Disertation\final\pushpa60_SORTED.csv"
OUTDIR = r"C:\Disertation\processed\Company_Analysis"
os.makedirs(OUTDIR, exist_ok=True)

# Load
df = pd.read_csv(DOM_FILE, low_memory=False)
meta = pd.read_csv(META_FILE, low_memory=False)

# Normalise keys
df['game_norm'] = df['game_norm'].astype(str).str.lower().str.strip()
meta['Game_Name_norm'] = meta['Game_Name'].astype(str).str.lower().str.strip()

# Map company into df via meta (left join)
meta_map = meta[['Game_Name_norm','Company']].drop_duplicates().set_index('Game_Name_norm')['Company'].to_dict()
df['Company'] = df['game_norm'].map(meta_map)

# 1. Top games by overall Dominance (mean across months)
overall_game = df.groupby('game_norm')['Dominance'].mean().reset_index().sort_values('Dominance', ascending=False)
print("\nTop 15 games by mean Dominance (overall):")
print(overall_game.head(15).to_string(index=False))

# 2. Top companies by mean Dominance (aggregate games → company then mean)
comp_dom = df.groupby('Company')['Dominance'].mean().reset_index().sort_values('Dominance', ascending=False)
print("\nTop 15 companies by mean Dominance:")
print(comp_dom.head(15).to_string(index=False))

# Save outputs
overall_game.to_csv(os.path.join(OUTDIR,"games_mean_dominance.csv"), index=False)
comp_dom.to_csv(os.path.join(OUTDIR,"companies_mean_dominance.csv"), index=False)

print("\nSaved CSVs to:", OUTDIR)
