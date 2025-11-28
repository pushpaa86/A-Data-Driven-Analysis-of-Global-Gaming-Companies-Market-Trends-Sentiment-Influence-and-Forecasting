import pandas as pd, os
DOM_FILE = r"C:\Disertation\processed\FINAL_with_Dominance_MONTHLY.csv"
OUTDIR = r"C:\Disertation\processed\Company_Analysis"
os.makedirs(OUTDIR, exist_ok=True)

df = pd.read_csv(DOM_FILE, low_memory=False)
df['game_norm'] = df['game_norm'].astype(str).str.lower().str.strip()

# mean sentiment and sd, mean users
agg = df.groupby('game_norm').agg(
    mean_sent=('avg_sentiment','mean'),
    sd_sent=('avg_sentiment','std'),
    mean_users=('Monthly_Active_Users_Millions','mean'),
    sd_users=('Monthly_Active_Users_Millions','std'),
    mean_dom=('Dominance','mean')
).reset_index()

print("\nTop 10 by mean sentiment:")
print(agg.sort_values('mean_sent', ascending=False)[['game_norm','mean_sent','sd_sent']].head(10).to_string(index=False))

print("\nTop 10 by mean monthly active users:")
print(agg.sort_values('mean_users', ascending=False)[['game_norm','mean_users','sd_users']].head(10).to_string(index=False))

# "Favorite" composite score — simple z-score average of sentiment and users
agg['sent_z'] = (agg['mean_sent'] - agg['mean_sent'].mean())/agg['mean_sent'].std(ddof=0)
agg['users_z'] = (agg['mean_users'] - agg['mean_users'].mean())/agg['mean_users'].std(ddof=0)
agg['fav_score'] = agg['sent_z'] + agg['users_z']
print("\nTop 10 by composite favourite score (sentiment + users):")
print(agg.sort_values('fav_score', ascending=False)[['game_norm','mean_sent','mean_users','fav_score']].head(10).to_string(index=False))

agg.to_csv(os.path.join(OUTDIR,"games_sentiment_users_summary.csv"), index=False)
print("\nSaved to:", OUTDIR)
