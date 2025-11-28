import pandas as pd, os, numpy as np
# Path to your manual forecast summary (adjust depending where you saved it)
SUM_FILE_CANDIDATES = [
    r"C:\Disertation\processed\Forecasts_manual\forecast_summary_manual.csv",
    r"C:\Disertation\processed\Forecasts\forecast_summary_manual.csv",
    r"C:\Disertation\processed\forecast_summary_manual.csv",
    r"C:\Disertation\processed\Forecasts\forecast_summary_manual.csv"
]
sum_file = None
for p in SUM_FILE_CANDIDATES:
    if os.path.exists(p):
        sum_file = p; break
if sum_file is None:
    raise FileNotFoundError("Forecast summary CSV not found; please provide its path.")

s = pd.read_csv(sum_file, low_memory=False)
# Filter valid numeric RMSEs
s['AR1_RMSE'] = pd.to_numeric(s['AR1_RMSE'], errors='coerce')
s['ARX_RMSE'] = pd.to_numeric(s['ARX_RMSE'], errors='coerce')

# Count comparisons (only where both available)
comp = s.dropna(subset=['AR1_RMSE','ARX_RMSE']).copy()
comp['improved'] = comp['ARX_RMSE'] < comp['AR1_RMSE']
n_total = len(comp)
n_improved = comp['improved'].sum()
pct_improved = 100.0 * n_improved / n_total if n_total>0 else float('nan')

print(f"\nForecast comparison over {n_total} games with both AR1 and ARX RMSEs:")
print(f"ARX improved over AR1 in {n_improved} games ({pct_improved:.1f}%)")

# Show games where ARX helped the most (largest AR1_RMSE - ARX_RMSE)
comp['delta'] = comp['AR1_RMSE'] - comp['ARX_RMSE']
print("\nTop 10 games where ARX (with sentiment) reduced RMSE the most:")
print(comp.sort_values('delta', ascending=False)[['game','AR1_RMSE','ARX_RMSE','delta']].head(10).to_string(index=False))

# Save
outdir = r"C:\Disertation\processed\Company_Analysis"
os.makedirs(outdir, exist_ok=True)
comp.to_csv(os.path.join(outdir,"forecast_AR1_vs_ARX_comparison.csv"), index=False)
print("\nSaved comparison to:", outdir)
