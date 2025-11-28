📊 A Data-Driven Analysis of Global Gaming Companies
Market Trends, Sentiment Influence & Forecasting (50 Games Project)

This project develops a sentiment-enhanced forecasting system for 50 global video games by combining player reviews, engagement indicators, and a custom dominance index.
It includes large-scale review scraping (500k+ reviews), monthly sentiment scoring, AR/ARX forecasting, trend analysis, and company-level insights.

🚀 Project Overview

This repository contains the full code pipeline used to:

Scrape Google Play & Steam reviews for 50 games

Compute cleaned sentiment scores using NLP rules, emojis & rating-adjustments

Aggregate monthly sentiment (2023–2025)

Calculate a multi-factor market dominance index

Generate manual & statistical forecasts using AR(1) and ARX (with sentiment/IP strength)

Analyse company-level dominance, correlations, and long-term trends

Visualize sentiment, dominance, and forecast patterns

The system demonstrates how player sentiment can meaningfully influence forecasting accuracy and company performance.

🧱 Repository Structure
├── AR1_RMSE vs ARX_RMSE.py                # Comparison of forecasting accuracy
├── Dominance_Top5_trends_FIXED.png        # Trend plot for top 5 dominant games
├── Top10_Dominance_overall.png            # Overall dominance ranking chart
│
├── aggregate_monthly_sentiment_allgames.py # Monthly sentiment aggregation pipeline
├── calculate_sentiment_score.py            # NLP-based sentiment scoring function
│
├── baldures_gate3_steam_scraper.py
├── elden_ring_scraper.py
├── append_cod_pubg_reviews_fixed.py        # Review scraping scripts (Play Store / Steam)
│
├── company_sentiment_dominance_analysis.py # Company-level dominance + correlation
├── company_and_game_summary.py
├── company analysis.py
│
├── minecraft_manual_forecast.png
├── elden_ring_manual_forecast.png
├── valorant_manual_forecast.png
├── the_witcher_3_manual_forecast.png       # Forecast visualisations
│
├── hist_sentiment_users_r.png              # Pearson r distribution plot
├── favourite — sentiment.py                # Misc sentiment experiment
│
├── selected 50 games.txt                   # Final game list
└── README.md

🔍 Key Features
1. Review Scraping (500k+ reviews)

Automated scripts for Steam & Google Play

2023–2025 review filtering

Saved CSV outputs per game

2. Custom Sentiment Scoring

Detects keywords, emojis, punctuation, and ratings

Produces a unified 1–10 sentiment scale

Works even when no numeric rating exists

3. Monthly Sentiment Aggregation

Processes large CSVs in memory-efficient chunks

Auto-detects date/text/sentiment columns

Outputs per-game monthly averages

4. Dominance Scoring Model

A four-factor normalized model:

Rating

Sentiment

Engagement (MAU)

IP Strength

Combined with equal weights into a single dominance index.

5. Forecasting (AR1 & ARX Models)

AR(1): Pure engagement-based

ARX: Engagement + sentiment + IP strength

RMSE evaluation

Shows when sentiment improves predictions

6. Company-Level Analysis

Game → Company mapping

Mean dominance across months

Revenue-weighted dominance

Sentiment → Engagement correlations

📈 Visual Outputs Included

✔ Monthly sentiment charts
✔ Dominance trends (Top 5 games)
✔ Top 10 dominant games (bar chart)
✔ AR/ARX forecast comparison
✔ Histograms of sentiment–user correlation

All plots are included in the repository.

🛠️ Tech Stack

Python 3.10+

pandas, numpy

matplotlib

scipy (optional)

google-play-scraper / steamdb scraping

regex / emoji parsing

▶️ How to Run
1. Install dependencies
pip install -r requirements.txt

2. Scrape reviews
python elden_ring_scraper.py
python baldures_gate3_steam_scraper.py

3. Aggregate sentiment
python aggregate_monthly_sentiment_allgames.py

4. Generate dominance scores

(Done inside analysis scripts)

5. Run forecasting
python AR1_RMSE vs ARX_RMSE.py

6. Company-level evaluation
python company_sentiment_dominance_analysis.py

📚 Main Insights From the Project

Sentiment improves forecasting accuracy for many games (ARX > AR1).

Some companies maintain strong long-term dominance driven by consistently high sentiment and user engagement.

Games with stable positive sentiment show more predictable trends.

Dominance modelling helps understand market share, player behaviour, and IP strength.

📬 Contact

For questions, collaboration, or opportunities:
Pushpanjali – Data Analyst / Machine Learning Enthusiast
📧 Email: pushpaanjali86@gmail.com
🌐 GitHub: https://github.com/pushpaa86
 Linkedin: https://www.linkedin.com/in/pushpanjali-mamidakula-160083220/
📧 Email: (add email)
🌐 GitHub: https://github.com/pushpaa86
