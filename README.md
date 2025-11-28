🎮 Sentiment-Enhanced Market Analysis & Forecasting for Global Gaming Companies

This project delivers an end-to-end data science pipeline for analyzing market trends in the global gaming industry.
It includes web scraping, sentiment scoring, trend analysis, dominance modelling, forecasting (AR / ARX), and company-level insights using real user reviews and engagement metrics.

🔹 Project Workflow
1. Data Collection (Scraping)

Python scripts scrape 500k+ reviews from Steam & Google Play for 50 selected games.
Scripts include:

elden_ring_scraper.py

baldurs_gate3_steam_scraper.py

append_cod_pubg_reviews_fixed.py

Example scraping output screenshot:
![Review Scraper](favourite — sentiment.png)

2. Sentiment Analysis Pipeline

The script calculate_sentiment_score.py applies:

Keyword scoring

Emoji scoring

Punctuation scoring

User rating adjustment

Outputs a unified 1–10 sentiment score.

Monthly aggregation is done using:

aggregate_monthly_sentiment_allgames.py

Visual output example:


3. Dominance Score Modelling

A 4-factor dominance index is computed for each game:

User Rating

Sentiment

Engagement (MAU)

IP Strength

All factors normalized and weighted equally.
Code: company_sentiment_dominance_analysis.py

Example visual:


4. Forecasting Models (AR & ARX)

Manual forecasting for major titles using:

AR(1) model

ARX (AR + sentiment + IP strength)

Script: AR1_RMSE vs ARX_RMSE.py

Example forecast charts:








5. Company-Level Analysis

Maps each game → its parent company to compute:

Mean dominance

Revenue-weighted dominance

Sentiment vs Engagement correlation

Script: company analysis.py
Trend example:


🔹 Repository Structure
A-Data-Driven-Analysis-of-Global-Gaming-Companies/
│── AR1_RMSE vs ARX_RMSE.py
│── aggregate_monthly_sentiment_allgames.py
│── calculate_sentiment_score.py
│── company_and_game_summary.py
│── company_sentiment_dominance_analysis.py
│── selected 50 games.txt
│── Top10_Dominance_overall.png
│── Dominance_Top5_trends_FIXED.png
│── elden_ring_manual_forecast.png
│── minecraft_manual_forecast.png
│── the_witcher_3_manual_forecast.png
│── valorant_manual_forecast.png
│── hist_sentiment_users_r.png
│── README.md

🔹 How to Run
1. Run Review Scrapers
python elden_ring_scraper.py
python baldures_gate3_steam_scraper.py

2. Aggregate Sentiment
python aggregate_monthly_sentiment_allgames.py

3. Generate Dominance Scores
python company_sentiment_dominance_analysis.py

4. Run Forecasting Models
python "AR1_RMSE vs ARX_RMSE.py"

🔹 Key Outcomes

Processed 500k+ player reviews

Built custom sentiment scoring algorithm

Created multi-factor dominance index

Forecasted engagement using AR & ARX

Found that sentiment improved forecasting accuracy for many games

Identified top companies & top games by market dominance
