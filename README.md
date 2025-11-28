# A-Data-Driven-Analysis-of-Global-Gaming-Companies-Market-Trends-Sentiment-Influence-and-Forecasting
 Built a sentiment-enhanced forecasting framework for 50 video games by scraping 500k+ reviews, generating monthly sentiment scores, calculating a multi-factor dominance index, and applying AR/ARX models. Delivered company-level insights, trend analysis, and accuracy improvements using real user sentiment.
🎮 Sentiment-Enhanced Forecasting & Market Dominance Analysis for Video Games

A Data Science Masters Project (7COM1075)

This project develops a sentiment-driven forecasting and market dominance analysis system for the video-game industry.
Using 50 top games, this study integrates player review sentiment, engagement metrics, IP strength, and company-level performance indicators into a unified analytical framework.

The system combines Python-based sentiment processing, time-series forecasting models (AR & ARX), and a novel dominance scoring formula to identify:

Which games maintain strong long-term player engagement

Which companies lead the market

Whether player sentiment improves forecasting accuracy

📂 Project Structure
├── data/
│   ├── reviews/                 # 10,000+ raw reviews per game
│   ├── FINAL_with_Dominance_MONTHLY.csv
│   ├── pushpa60_SORTED.csv      # Company mapping file
│
├── src/
│   ├── sentiment_scoring.py     # Custom keyword + emoji + punctuation model
│   ├── scrape_reviews.py        # Google Play & Steam scraping script
│   ├── aggregate_monthly.py     # Monthly sentiment aggregation
│   ├── dominance_model.py       # Dominance formula & normalization
│   ├── forecasting_AR_ARX.py    # AR & ARX forecasting + RMSE evaluation
│   ├── company_analysis.py      # Company-level dominance & correlations
│
├── results/
│   ├── dashboards/
│   ├── forecasting_charts/
│   ├── company_analysis/
│
└── README.md

🧠 Key Features
✔️ 1. Review Scraping (10,000 newest reviews per game)

Google Play Scraper (Python)

Steam Review API

Unified dataset created for 50 selected games
(See Appendix A for the full game list.)

✔️ 2. Custom Sentiment Scoring Model

A hybrid NLP approach combining:

Keyword dictionary (positive/negative, strong/mild)

Emoji impact

Punctuation weighting (!, ?)

Optional user rating adjustment

Produces a 1–10 sentiment score for every review.

✔️ 3. Monthly Sentiment Aggregation

Reads large CSVs in chunks

Detects date/text columns automatically

Outputs per-game monthly average sentiment + review counts

✔️ 4. Dominance Score Model

Novel metric using 4 equally weighted factors:

Variable	Meaning
R_norm	Normalized User Rating
S_norm	Normalized Sentiment
U_norm	Normalized User Engagement
I_norm	Normalized IP Strength

Dominance = 0.25(R + S + U + I)

✔️ 5. Forecasting Models (AR & ARX)

AR(1) → uses only past engagement

ARX → adds sentiment + IP strength as predictors

RMSE used for model evaluation

📌 Finding:
Sentiment improves forecasting accuracy for many games (ARX < AR RMSE).

✔️ 6. Company-Level Analytics

Maps each game → parent company

Aggregates dominance and engagement across months

Calculates Pearson correlations

Identifies top-performing companies

📌 Finding:
Some companies consistently show high sentiment + high engagement, demonstrating true market leadership.

📊 Key Research Questions Answered
1️⃣ Does sentiment improve forecasting accuracy?

✔ Yes. ARX performed better (lower RMSE) for many games.

2️⃣ Which companies lead the market?

✔ Based on dominance + revenue-weighted metrics, a few companies stand out consistently.

3️⃣ Which games maintain strong long-term preference?

✔ Games with high sentiment also show high engagement stability.

📐 Mathematical Models Used

Min–Max Normalisation

Dominance Score Formula

AR(1) Time-Series Model

ARX Model with Exogenous Inputs

Holt Linear Trend (long-term trend detection)

Pearson Correlation

RMSE Accuracy Metric

🚀 How to Run the Project
Install dependencies
pip install -r requirements.txt

1. Scrape reviews
python scrape_reviews.py

2. Compute sentiment
python sentiment_scoring.py

3. Aggregate monthly data
python aggregate_monthly.py

4. Generate dominance scores
python dominance_model.py

5. Run forecasting
python forecasting_AR_ARX.py

6. Company analysis
python company_analysis.py

📦 Results & Outputs

All outputs are available in the results/ folder:

Monthly Sentiment Dataset

Dominance Tables

AR vs ARX Forecasting Charts

Company Rankings

Pearson Correlation Reports

Visual Dashboards


🤝 Contact

If you found this project useful, feel free to connect on LinkedIn or GitHub!
