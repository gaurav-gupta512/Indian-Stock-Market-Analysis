# Indian-Stock-Market-Analysis
Machine Coding Challenge from MagiProp sent on 22nd November 12 PM

NIFTY 50 Intraday Price & OI Analysis

A Python tool to identify NIFTY 50 stocks with the highest positive correlation between Price and Open Interest (OI) changes, indicating potential trend continuations.

Setup

Install the required libraries:

pip install pandas numpy requests lxml


Usage

1. Generate Data
Scrapes the stock list and generates synthetic intraday data:

python fetch_data.py


2. Analyze Correlations
Calculates correlations and prints the top 5 stocks:

python analyze_data.py


How It Works

fetch_data.py: Dynamically fetches the NIFTY 50 stock list from Wikipedia and simulates 5-minute intraday price/OI data (saved to intraday_data.csv).

analyze_data.py: Calculates the Pearson correlation between Price % Change and OI % Change over the last 60 minutes.

Note: This tool uses synthetic data for demonstration purposes. Do not use the output for actual trading.
