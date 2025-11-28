import pandas as pd
import numpy as np

# ========= FILE PATHS =========
dom_file = r"C:\Disertation\processed\FINAL_with_Dominance_MONTHLY.csv"
company_file = r"C:\Disertation\final\pushpa60_SORTED.csv"

# ========= LOAD FILES =========
df = pd.read_csv(dom_file)
df2 = pd.read_csv(company_file)

# Clean company file
df2 = df2.rename(columns={'ï»¿Date':'Date'})
df2['game_norm'] = df2['Game_Name'].str.lower().str.strip()

# Build mapping (unique game -> company)
mapping = df2[['game_norm','Company']].drop_duplicates()

print("\n=== GAME → COMPANY MAPPING CREATED ===\n")
print(mapping.head(20))

# ========= MERGE COMPANY INTO DOMINANCE DATA =========
df['game_norm'] = df['game_norm'].str.lower().str.strip()

merged = df.merge(mapping, on='game_norm', how='left')

print("\nMerged shape:", merged.shape)
print("Null companies:", merged['Company'].isna().sum())

# ========= COMPANY LEVEL DOMINANCE =========
company_dom = (
    merged.groupby('Company')['Dominance']
          .agg(['mean','max','min','std','count'])
          .rename(columns={'mean':'dom_mean','count':'months'})
          .sort_values('dom_mean', ascending=False)
)

print("\n=== COMPANY DOMINANCE TABLE ===\n")
print(company_dom.head(10))

# ========= COMPANY LEVEL SENTIMENT CORRELATION =========
def safe_corr(a, b):
    if len(a) < 3 or np.nanstd(a)==0 or np.nanstd(b)==0:
        return np.nan
    return float(np.corrcoef(a, b)[0,1])

corr_rows = []
for comp, grp in merged.groupby('Company'):
    corr_sent_user = safe_corr(grp['avg_sentiment'], grp['Monthly_Active_Users_Millions'])
    corr_sent_dom  = safe_corr(grp['avg_sentiment'], grp['Dominance'])
    
    corr_rows.append({
        'Company': comp,
        'Corr(Sent vs Users)': corr_sent_user,
        'Corr(Sent vs Dominance)': corr_sent_dom
    })

company_corr = pd.DataFrame(corr_rows).sort_values('Corr(Sent vs Dominance)', ascending=False)

print("\n=== COMPANY SENTIMENT CORRELATION ===\n")
print(company_corr.head(10))

# ========= SAVE OUTPUTS =========
out_dir = r"C:\Disertation\processed\Company_Analysis"
import os; os.makedirs(out_dir, exist_ok=True)

company_dom.to_csv(out_dir + r"\company_dominance.csv")
company_corr.to_csv(out_dir + r"\company_sentiment_correlation.csv")

print("\nSaved company analysis to:", out_dir)
