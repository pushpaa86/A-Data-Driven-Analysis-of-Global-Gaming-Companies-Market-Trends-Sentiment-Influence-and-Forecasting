🎮 A Data-Driven Analysis of Global Gaming Companies – Market Trends, Sentiment Influence & Forecasting

This project builds a complete analytics + forecasting framework for the global gaming industry by scraping 500,000+ real user reviews, generating monthly sentiment scores, computing a multi-factor dominance index, and applying AR/ARX forecasting models using real sentiment signals.

🔷 Project Workflow
1. Data Collection (Web Scraping)

Scraped reviews from Google Play & Steam for 50 games.

Scripts used:

eldon_ring_scraper.py

baldurres_gate3_steam_scraper.py

append_cod_pubg_reviews_fixed.py

fortnite_mobile_reviews.py

compare_pushpa60_reviews.py

and more…

⬇️ Output: Cleaned review datasets (*.csv), ~500k reviews.

🔷 2. Sentiment Scoring (Python)

Script: calculate_sentiment_score.py

Sentiment computed using:

Keyword intensity (strong + mild positive/negative words)

Emoji sentiment

Punctuation impact (e.g., “!!!!!”, “???”)

User ratings

Final scale: 1–10 sentiment score

🔷 3. Monthly Sentiment Aggregation

Script: aggregate_monthly_sentiment_allgames.py

Pipeline performs:

Auto-detect date columns

Chunk-based reading for large files

Monthly average sentiment per game

Review count aggregation

⬇️ Output:
monthly_sentiment_50games.csv
aggregation_log.csv

🔷 4. Dominance Score Calculation

Script: Part of company sentiment & dominance pipeline

Normalizes 4 factors (sentiment, users, revenue, IP strength)

Applies equal weights

Computes 0–1 dominance score

📈 Included visual outputs:

Dominance_Top5_trends_FIXED.png

Top10_Dominance_overall.png

🔷 5. Forecasting (AR & ARX Models)

Script: AR1_RMSE vs ARX_RMSE.py

Forecast types:

AR(1) → baseline (past engagement only)

ARX → adds sentiment + IP strength

Outputs:

RMSE comparison

Forecast graphs:

elden_ring_manual_forecast.png

minecraft_manual_forecast.png

valorant_manual_forecast.png

the_witcher_3_manual_forecast.png

🔷 6. Company-Level Insights

Scripts:

company_and_game_summary.py

company_sentiment_dominance_analysis.py

company analysis.py

Analysis includes:

Market dominance per company

Sentiment → Users correlation

Revenue-weighted dominance

Top games per company

Outputs include:

company_dominance_summary.csv

hist_sentiment_users_r.png

🗂 Repository Structure
A-Data-Driven-Analysis-of-Global-Gaming/
│── eldon_ring_scraper.py
│── baldures_gate3_steam_scraper.py
│── append_cod_pubg_reviews_fixed.py
│── calculate_sentiment_score.py
│── aggregate_monthly_sentiment_allgames.py
│── company_sentiment_dominance_analysis.py
│── company_and_game_summary.py
│── AR1_RMSE vs ARX_RMSE.py
│── Top10_Dominance_overall.png
│── Dominance_Top5_trends_FIXED.png
│── */manual_forecast.png (for 4–5 games)
│── selected 50 games.txt
│── README.md

🖥 How to Run the Project
1. Run Scrapers
python eldon_ring_scraper.py
python baldures_gate3_steam_scraper.py

2. Sentiment Scoring
python calculate_sentiment_score.py

3. Aggregate Monthly Sentiment
python aggregate_monthly_sentiment_allgames.py

4. Compute Dominance
python company_sentiment_dominance_analysis.py

5. Run Forecast Models
python "AR1_RMSE vs ARX_RMSE.py"

📷 Example Visualizations
Top 10 Overall Dominance

Dominance Trends (Top 5 Games)

Forecast Example (Elden Ring)

Sentiment vs Users Correlation Histogram

⭐ Key Outcomes

Scraped 500k+ reviews and created 50 monthly sentiment timelines

Built a custom sentiment scoring engine (1–10 scale)

Designed a multi-factor dominance index

ARX models improved forecasting accuracy in 70%+ games

Identified top companies by dominance and sentiment impact
