# aggregate_monthly_sentiment_allgames.py
# Usage: py aggregate_monthly_sentiment_allgames.py
import os
import pandas as pd
import numpy as np
from glob import glob
import chardet      # optional but helpful; pip install chardet
import csv
from datetime import datetime

# CONFIG - update paths if needed
REVIEWS_FOLDER = r"C:\Disertation\reviews\game reviews"
OUTPUT_CSV = r"C:\Disertation\processed\monthly_sentiment_50games.csv"
LOG_CSV = r"C:\Disertation\processed\aggregation_log.csv"
CHUNKSIZE = 200000   # adjust for memory / speed

# small keyword fallback estimator (used only if no sentiment column and no numeric score)
keyword_weights = {
    'excellent': 2, 'love': 2, 'great': 1.5, 'good': 1, 'fun': 1,
    'awesome':1.5, 'amazing':2, 'best':2,
    'hate': -2, 'broken': -1.5, 'bad': -1, 'lag': -1.5, 'crash': -2,
    'bug': -1.5, 'slow': -1, 'disappoint': -1.5
}

def estimate_sentiment_from_text(text):
    text = str(text).lower()
    score = 5.0  # base midpoint (range 1..10)
    for kw, w in keyword_weights.items():
        if kw in text:
            score += w
    return max(1.0, min(10.0, score))

def detect_encoding(path, nbytes=10000):
    # try chardet if available (robust detection for non-utf files)
    try:
        with open(path, 'rb') as f:
            raw = f.read(nbytes)
        res = chardet.detect(raw)
        enc = res.get('encoding') or 'utf-8'
        return enc
    except Exception:
        return 'utf-8'

def try_read_head(path, nrows=5):
    # Try common separators and encodings, return dataframe or raise
    enc = detect_encoding(path)
    for sep in [',',';','\t','|']:
        try:
            return pd.read_csv(path, nrows=nrows, sep=sep, encoding=enc, low_memory=False)
        except Exception:
            continue
    # final fallback
    return pd.read_csv(path, nrows=nrows, encoding=enc, low_memory=False)

def find_date_column(cols):
    lower = [c.lower() for c in cols]
    for candidate in ['at','timestamp','time','date','created','reviewcreated','submitted','postedat','created_at','posted_at']:
        if candidate in lower:
            return cols[lower.index(candidate)]
    # fallback: any column containing 'time' or 'date'
    for i,c in enumerate(lower):
        if 'time' in c or 'date' in c:
            return cols[i]
    return None

def find_text_column(cols):
    lower = [c.lower() for c in cols]
    for candidate in ['content','review','comment','body','text']:
        if candidate in lower:
            return cols[lower.index(candidate)]
    return None

def find_sentiment_column(cols):
    lower = [c.lower() for c in cols]
    for candidate in ['sentiment','sentiment_score','sentiment_score_value']:
        if candidate in lower:
            return cols[lower.index(candidate)]
    return None

def find_score_column(cols):
    lower = [c.lower() for c in cols]
    for candidate in ['score','rating','stars','rate']:
        if candidate in lower:
            return cols[lower.index(candidate)]
    return None

# iterate files and aggregate
aggregates = []   # list of dataframes to concat
log_records = []
files = sorted([f for f in os.listdir(REVIEWS_FOLDER) if f.lower().endswith('.csv')])
if not files:
    raise SystemExit(f"No CSVs found in {REVIEWS_FOLDER}")

for fn in files:
    path = os.path.join(REVIEWS_FOLDER, fn)
    filesize = os.path.getsize(path)
    record = {'file': fn, 'size_bytes': filesize, 'status': 'ok', 'rows_processed': 0}
    if filesize < 50:   # tiny/empty file
        record['status'] = 'empty_or_too_small'
        log_records.append(record)
        print(f"Skipping (empty/small): {fn}")
        continue

    try:
        # Read head to detect columns & separator/encoding
        head = try_read_head(path, nrows=5)
    except Exception as e:
        record['status'] = f'error_read_head: {e}'
        log_records.append(record)
        print(f"Error reading head of {fn}: {e}")
        continue

    cols = list(head.columns)
    date_col = find_date_column(cols)
    text_col = find_text_column(cols)
    sent_col = find_sentiment_column(cols)
    score_col = find_score_column(cols)

    # Determine game name from filename (strip extension)
    game_name = os.path.splitext(fn)[0].strip()

    # Read in chunks for memory-efficiency
    month_rows = []  # will collect per-chunk aggregates
    try:
        enc = detect_encoding(path)
        # try separators
        reader = None
        for sep in [',',';','\t','|']:
            try:
                reader = pd.read_csv(path, chunksize=CHUNKSIZE, encoding=enc, sep=sep, low_memory=False)
                # quick sanity check: first chunk should have expected cols
                first = next(reader)
                # restore iterator (create new)
                reader = pd.read_csv(path, chunksize=CHUNKSIZE, encoding=enc, sep=sep, low_memory=False)
                break
            except Exception:
                reader = None
                continue
        if reader is None:
            raise ValueError("Unable to read file with common separators")

        for chunk in reader:
            # unify columns
            chunk.columns = [c.strip() for c in chunk.columns]

            # pick date col
            if date_col and date_col in chunk.columns:
                dcol = date_col
            else:
                # attempt to auto-detect in chunk
                dcol = find_date_column(chunk.columns)
            if dcol is None:
                # cannot find timestamps in this file -> skip
                continue

            # parse datetime
            chunk[dcol] = pd.to_datetime(chunk[dcol], errors='coerce', utc=True)
            chunk = chunk.dropna(subset=[dcol])    # drop rows with no date
            if chunk.empty:
                continue

            # determine sentiment per row
            if sent_col and sent_col in chunk.columns:
                chunk['sentiment_score'] = pd.to_numeric(chunk[sent_col], errors='coerce')
            elif score_col and score_col in chunk.columns:
                # map store score range to 1..10 (best-effort)
                # detect typical scale: if max <=5 assume 1-5 scale; if <=10 assume 1-10 else rescale
                sc = pd.to_numeric(chunk[score_col], errors='coerce')
                maxv = sc.max(skipna=True)
                minv = sc.min(skipna=True)
                if pd.notna(maxv) and maxv <= 5:
                    chunk['sentiment_score'] = ((sc - minv) / (maxv - minv)) * 9 + 1
                elif pd.notna(maxv) and maxv <= 10:
                    chunk['sentiment_score'] = sc  # already ~1..10
                else:
                    # generic min-max to 1..10
                    chunk['sentiment_score'] = ((sc - minv) / (maxv - minv)) * 9 + 1
            elif text_col and text_col in chunk.columns:
                chunk['sentiment_score'] = chunk[text_col].apply(estimate_sentiment_from_text)
            else:
                # no way to compute sentiment -> skip chunk
                continue

            # month key
            chunk['year_month'] = chunk[dcol].dt.to_period('M').astype(str)

            # set game column if not present
            if 'game' not in chunk.columns:
                chunk['game'] = game_name

            agg = chunk.groupby(['game','year_month'])['sentiment_score'].agg(['mean','count']).reset_index()
            agg.rename(columns={'mean':'avg_sentiment','count':'review_count'}, inplace=True)
            month_rows.append(agg)
            record['rows_processed'] += len(chunk)

        if month_rows:
            df_file = pd.concat(month_rows, ignore_index=True)
            # reduce by regrouping (some months may be repeated from multiple chunks)
            df_file = df_file.groupby(['game','year_month']).agg({'avg_sentiment':'mean','review_count':'sum'}).reset_index()
            aggregates.append(df_file)
            record['status'] = 'aggregated'
        else:
            record['status'] = 'no_valid_rows'
        log_records.append(record)
        print(f"Processed {fn}: status={record['status']} rows={record['rows_processed']}")

    except Exception as e:
        record['status'] = f'error:{e}'
        log_records.append(record)
        print(f"Error processing {fn}: {e}")

# combine all aggregates
if aggregates:
    all_df = pd.concat(aggregates, ignore_index=True)
    all_df = all_df.groupby(['game','year_month']).agg({'avg_sentiment':'mean','review_count':'sum'}).reset_index()
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    all_df.to_csv(OUTPUT_CSV, index=False)
    print("Wrote aggregated monthly sentiment to:", OUTPUT_CSV)
else:
    print("No aggregates created (no valid data).")

# write log
os.makedirs(os.path.dirname(LOG_CSV), exist_ok=True)
pd.DataFrame(log_records).to_csv(LOG_CSV, index=False)
print("Wrote log to:", LOG_CSV)
