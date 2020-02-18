# Bootcamp_repo_portfolio
Bootcamp project portfolio optimization

Project design and created in 3 days during data science course.
Objective : Portfolio optimization using clustering solutions (Hierarchical Clustering, K-Mean) and a variance optimization process (Markovitz 1952).
Limitations: Variance optimization process are hit by exponentially increasing bias.

Step 1: Extract S&P500 market data (Open High Low Close, OHLC) from API (survival bias here)

Step 2: Hiearchical clustering of companies (5 clusters retained)

Step 3: Creation of equally weighted portfolio among clusters (1/N, DeMiguel, Garlappi)

Step 4: Markovitz optimization process among those 5 clusters to reduce estimatino bias (Maximum sharpe ratio retained)

Step 5: Results analysis, benchmark comparison
