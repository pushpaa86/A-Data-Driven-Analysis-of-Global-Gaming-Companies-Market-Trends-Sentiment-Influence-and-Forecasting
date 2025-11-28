# company_sentiment_dominance_analysis.py
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Try to import scipy for p-values; if not available, continue gracefully
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False

# ---------- CONFIG ----------
INPUT_CANDIDATES = [
    r"C:\Disertation\processed\FINAL_with_Dominance_MONTHLY.csv",
    r"C:\Disertation\processed\FINAL_50games_MONTHLY_INTERPOLATED.csv",
    r"C:\Disertation\processed\FINAL_50games_merged.csv",
    r"C:\Disertation\final\pushpa60_SORTED.csv"
]
OUT_DIR = r"C:\Disertation\processed\Company_Analysis"
os.makedirs(OUT_DIR, exist_ok=True)

# Column names (adapt if your files differ)
GAME_COL = "game_norm"
COMPANY_COL = "Company"               # present in pushpa60_SORTED.csv / merged file
DATE_COL = "year_month"               # YYYY-MM or full date
SENT_COL = "avg_sentiment"
USERS_COL = "Monthly_Active_Users_Millions"
REVENUE_COL = "Monthly_Revenue_USD_Millions"
DOM_COL = "Dominance"

MIN_MONTHS_FOR_CORR = 6  # minimum months to compute correlation

# ---------- Helpers ----------
def try_load_first(paths):
    for p in paths:
        if os.path.exists(p):
            print("Loading:", p)
            return pd.read_csv(p, low_memory=False)
    raise FileNotFoundError(f"None of the input files found. Checked: {paths}")

def to_ym(x):
    # normalize to YYYY-MM
    try:
        return pd.to_datetime(x).strftime("%Y-%m")
    except Exception:
        return str(x)[:7]

def pearson_with_p(x, y):
    # returns r, p (p may be np.nan if scipy not available)
    if len(x) < 2:
        return np.nan, np.nan
    x = np.array(x); y = np.array(y)
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() < 2:
        return np.nan, np.nan
    xr = x[mask]; yr = y[mask]
    if xr.std() == 0 or yr.std() == 0:
        return np.nan, np.nan
    r = np.corrcoef(xr, yr)[0,1]
    p = np.nan
    if SCIPY_AVAILABLE:
        try:
            p = stats.pearsonr(xr, yr)[1]
        except Exception:
            p = np.nan
    else:
        # compute t-statistic and p approx using Student t distribution formula if possible
        try:
            n = len(xr)
            t = r * np.sqrt((n-2)/(1-r*r))
            # can't compute p without CDF; leave as NaN
            p = np.nan
        except Exception:
            p = np.nan
    return float(r), p

# ---------- Main ----------
def main():
    df = try_load_first(INPUT_CANDIDATES)

    # Ensure expected columns exist; try to map alternatives
    if DATE_COL not in df.columns:
        for cand in ["Date", "date", "ds", "year_month"]:
            if cand in df.columns:
                df[DATE_COL] = df[cand]
                break

    if GAME_COL not in df.columns:
        if "Game_Name" in df.columns:
            df[GAME_COL] = df["Game_Name"].str.lower().str.strip()
        elif "game" in df.columns:
            df[GAME_COL] = df["game"].str.lower().str.strip()
        else:
            raise KeyError("No game name column found. Expected 'game_norm' or 'Game_Name' or 'game'.")

    # company column mapping: if missing, try to load from other candidate file
    if COMPANY_COL not in df.columns:
        # try loading pushpa60_SORTED if present
        fallback = r"C:\Disertation\final\pushpa60_SORTED.csv"
        if os.path.exists(fallback):
            meta = pd.read_csv(fallback, low_memory=False)
            if 'Game_Name' in meta.columns and 'Company' in meta.columns:
                meta['game_norm'] = meta['Game_Name'].str.lower().str.strip()
                mapping = meta.set_index('game_norm')['Company'].to_dict()
                df[COMPANY_COL] = df[GAME_COL].map(mapping)
                print("Mapped Company from pushpa60_SORTED.csv")
    # normalize date to ym
    df[DATE_COL] = df[DATE_COL].astype(str).apply(to_ym)

    # normalize game names lower
    df[GAME_COL] = df[GAME_COL].astype(str).str.lower().str.strip()

    # Ensure numeric cols exist
    for col in [SENT_COL, USERS_COL, REVENUE_COL, DOM_COL]:
        if col not in df.columns:
            df[col] = np.nan

    # ---------- Per-game sentiment vs users correlation ----------
    games = sorted(df[GAME_COL].unique())
    corr_rows = []
    lag_corr_rows = []
    for g in games:
        sub = df[df[GAME_COL] == g].sort_values(DATE_COL)
        # need at least MIN_MONTHS_FOR_CORR rows
        if len(sub) < MIN_MONTHS_FOR_CORR:
            continue
        # direct correlation: sentiment vs users (same month)
        r, p = pearson_with_p(sub[SENT_COL].values, sub[USERS_COL].values)
        corr_rows.append({
            'game': g, 'n_months': len(sub), 'pearson_r': r, 'pearson_p': p,
            'sent_mean': float(np.nanmean(sub[SENT_COL])),
            'users_mean': float(np.nanmean(sub[USERS_COL]))
        })
        # lagged correlation sentiment_{t-1} vs users_t
        sent_lag = sub[SENT_COL].shift(1).values
        users = sub[USERS_COL].values
        r2, p2 = pearson_with_p(sent_lag, users)
        lag_corr_rows.append({
            'game': g, 'n_months': len(sub), 'pearson_r_lag1': r2, 'pearson_p_lag1': p2
        })

    corr_df = pd.DataFrame(corr_rows).sort_values('pearson_r', ascending=False)
    lag_corr_df = pd.DataFrame(lag_corr_rows).sort_values('pearson_r_lag1', ascending=False)

    corr_df.to_csv(os.path.join(OUT_DIR, "per_game_sentiment_users_corr.csv"), index=False)
    lag_corr_df.to_csv(os.path.join(OUT_DIR, "per_game_sentiment_users_lag1_corr.csv"), index=False)
    print("Saved per-game correlation tables to:", OUT_DIR)

    # Save histogram of correlation coefficients
    plt.figure(figsize=(7,5))
    vals = corr_df['pearson_r'].dropna()
    if len(vals) > 0:
        plt.hist(vals, bins=18)
        plt.title("Distribution of per-game Pearson r (sentiment vs users)")
        plt.xlabel("Pearson r")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, "hist_sentiment_users_r.png"), dpi=200)
        plt.close()

    # ---------- Company-level dominance ----------
    # Need company info: map games -> company
    if COMPANY_COL not in df.columns or df[COMPANY_COL].isna().all():
        print("Warning: Company column missing or empty. Company-level aggregation will be 'unknown' unless you provide mapping.")
        df[COMPANY_COL] = df.get(COMPANY_COL).fillna("unknown")

    # For company-level aggregation we need Dominance column and optionally revenue for weighting
    # compute two variants: mean(Dominance) and revenue-weighted mean across (game,month) aggregated per company (average over time)
    # First ensure dominance numeric
    df[DOM_COL] = pd.to_numeric(df[DOM_COL], errors='coerce')
    df[REVENUE_COL] = pd.to_numeric(df[REVENUE_COL], errors='coerce')
    df[USERS_COL] = pd.to_numeric(df[USERS_COL], errors='coerce')

    # Aggregate per company-month: average across games (some companies have multiple games in a month)
    comp_month = df.groupby([COMPANY_COL, DATE_COL]).agg({
        DOM_COL: 'mean',
        REVENUE_COL: 'sum',          # company revenue that month (sum over their games)
        USERS_COL: 'sum'             # total active users across company's games that month
    }).reset_index().rename(columns={DOM_COL: 'company_dom_mean_monthly'})

    # Overall company metrics: mean dominance across months, and revenue-weighted dominance
    # revenue-weighted dominance across company-months: weight by company revenue that month
    overall = comp_month.groupby(COMPANY_COL).apply(
        lambda g: pd.Series({
            'months': len(g),
            'dom_mean': float(g['company_dom_meanly'] ) if 'company_dom_meanly' in g.columns else float(g['company_dom_meanly'].mean()) if False else float(g['company_dom_meanly'].mean()) # dummy for compatibility
        })
    ).reset_index()

    # The above lambda uses a compatibility guard; we'll compute properly next:
    overall = comp_month.groupby(COMPANY_COL).agg({
        'company_dom_mean_monthly': ['mean', 'count'],
        REVENUE_COL: 'mean',
        USERS_COL: 'mean'
    })
    overall.columns = ['dom_monthly_mean', 'n_months', 'avg_monthly_revenue', 'avg_monthly_users']
    overall = overall.reset_index()

    # revenue-weighted dominance at company-level: for each company-month, dominance * revenue, summed / total revenue
    comp_month['rev_dom'] = comp_month['company_dom_mean_monthly'] * comp_month[REVENUE_COL]
    rev_weighted = comp_month.groupby(COMPANY_COL).agg({
        'rev_dom': 'sum',
        REVENUE_COL: 'sum',
        'company_dom_mean_monthly': 'mean'
    }).reset_index().rename(columns={'company_dom_mean_monthly':'dom_simple_mean'})
    rev_weighted['dom_revenue_weighted'] = rev_weighted.apply(
        lambda r: (r['rev_dom'] / r[REVENUE_COL]) if r[REVENUE_COL] > 0 else r['dom_simple_mean'], axis=1)

    # Merge overall and revenue-weighted
    company_df = overall.merge(rev_weighted[[COMPANY_COL, 'dom_revenue_weighted']], on=COMPANY_COL, how='left')
    company_df = company_df.sort_values('dom_revenue_weighted', ascending=False)

    company_df.to_csv(os.path.join(OUT_DIR, "company_dominance_summary.csv"), index=False)
    print("Saved company-level dominance summary to:", os.path.join(OUT_DIR, "company_dominance_summary.csv"))

    # Plot top companies by revenue-weighted dominance (top 10)
    topn = company_df.head(10)
    if not topn.empty:
        plt.figure(figsize=(8,5))
        plt.barh(topn[COMPANY_COL].astype(str)[::-1], topn['dom_revenue_weighted'][::-1])
        plt.xlabel("Revenue-weighted Dominance (0-1)")
        plt.title("Top 10 Companies by Revenue-weighted Dominance")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, "Top10_companies_dom_weighted.png"), dpi=200)
        plt.close()

    # Also save a table of top games per company (by overall game mean dominance)
    game_dom = df.groupby([GAME_COL]).agg({
        DOM_COL: 'mean'
    }).reset_index().sort_values(DOM_COL, ascending=False)
    # map game->company
    # if we have company mapping in original df, take most frequent company per game
    game_company_map = df.groupby(GAME_COL)[COMPANY_COL].agg(lambda x: x.dropna().mode().iloc[0] if len(x.dropna())>0 else "unknown").reset_index()
    game_dom = game_dom.merge(game_company_map, on=GAME_COL, how='left').rename(columns={COMPANY_COL:'company'})
    game_dom.to_csv(os.path.join(OUT_DIR, "games_mean_dominance_with_company.csv"), index=False)

    # Save correlation top lists
    corr_df.to_csv(os.path.join(OUT_DIR, "per_game_sentiment_users_corr.csv"), index=False)
    lag_corr_df.to_csv(os.path.join(OUT_DIR, "per_game_sentiment_users_lag1_corr.csv"), index=False)

    # Print short summary to console
    print("\n==== Quick Summary ====")
    print("Number of games with correlation computed:", len(corr_df))
    if not corr_df.empty:
        top_pos = corr_df.iloc[0]
        print("Best positive sentiment↔users (same month):", top_pos['game'], "r=", round(top_pos['pearson_r'],3), "p=", top_pos['pearson_p'])
        top_lag = lag_corr_df.iloc[0]
        print("Best lagged sentiment->users (lag1):", top_lag['game'], "r=", round(top_lag['pearson_r_lag1'],3), "p=", top_lag['pearson_p_lag1'])
    print("Top companies by revenue-weighted dominance (saved in company_dominance_summary.csv):")
    print(company_df[[COMPANY_COL, 'dom_revenue_weighted']].head(10).to_string(index=False))

    print("\nAll outputs saved to folder:", OUT_DIR)
    print("Files of interest:")
    for f in os.listdir(OUT_DIR):
        print(" -", f)

if __name__ == "__main__":
    main()
