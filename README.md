🎮 A Data-Driven Analysis of Global Gaming Companies – Market Trends, Sentiment Influence & Forecasting

This project builds an end-to-end analytical and forecasting framework for the global gaming industry by scraping 500,000+ player reviews, generating monthly sentiment scores, computing a multi-factor dominance index, and applying AR/ARX forecasting models using real user sentiment.

🔹 Project Workflow
1. Data Collection

Scraped reviews from Google Play & Steam for 50 games
Scripts used:

eldon_ring_scraper.py

baldurres_gate3_steam_scraper.py

append_cod_pubg_reviews_fixed.py

➡️ Output files include cleaned review datasets (CSV).

2. Sentiment Scoring (Python)

Script: calculate_sentiment_score.py

Computes sentiment using:

Keyword intensity

Emojis

Punctuation

User rating (1–5 scaled to 1–10)

➡️ Produces sentiment_score per review.

3. Monthly Sentiment Aggregation

Script: aggregate_monthly_sentiment_allgames.py

Converts raw reviews → monthly averages

Handles:

Encoding detection

Chunk-based loading

Automatic column detection

Score-to-sentiment conversion

➡️ Output: monthly_sentiment_50games.csv

4. Dominance Score System

Normalises 4 factors using Min–Max formula:

Avg Sentiment

Active Users

Revenue

Engagement

Weighted equally (0.25 each)

Script: company_and_game_summary.py

➡️ Output:

FINAL_with_Dominance_MONTHLY.csv

Trend charts like:

5. Forecasting (AR & ARX Models)

Scripts:

manual_forecast_pipeline.py

AR1_RMSE vs ARX_RMSE.py

Models Used:

AR(1): historical engagement

ARX: engagement + sentiment + IP strength

Generates:

Forecast curves

RMSE comparison

Example forecast:

6. Company-Level Analysis

Script: company_sentiment_dominance_analysis.py

Computes:

Company dominance

Sentiment correlation with users

Revenue-weighted dominance

Top games per company

Example outputs:

🔹 Repository Structure
A-Data-Driven-Analysis-of-Global-Gaming-Companies/
│── calculate_sentiment_score.py
│── aggregate_monthly_sentiment_allgames.py
│── company_sentiment_dominance_analysis.py
│── manual_forecast_pipeline.py
│── AR1_RMSE vs ARX_RMSE.py
│── selected 50 games.txt
│── Dominance_Top5_trends_FIXED.png
│── Top10_Dominance_overall.png
│── elden_ring_manual_forecast.png
│── minecraft_manual_forecast.png
│── the_witcher_3_manual_forecast.png
│── valorant_manual_forecast.png
│── hist_sentiment_users_r.png
│── README.md

🔹 How to Run
1. Install Dependencies
pip install pandas numpy matplotlib scipy

2. Run Sentiment Scoring
python calculate_sentiment_score.py

3. Aggregate Monthly Sentiment
python aggregate_monthly_sentiment_allgames.py

4. Compute Dominance Scores
python company_and_game_summary.py

5. Run Forecasts
python manual_forecast_pipeline.py

6. Company Analysis
python company_sentiment_dominance_analysis.py

🔹 Key Outcomes

✔ Scraped 500k+ player reviews

✔ Built a custom sentiment model

✔ Designed a cross-game dominance metric

✔ Forecasted engagement using AR & ARX models

✔ Identified top-performing games & companies

✔ Conducted sentiment–engagement correlation analysis

🔹 Contact

For queries, collaborations, or feedback:
📧 pushpaanjali86@gmail.com

