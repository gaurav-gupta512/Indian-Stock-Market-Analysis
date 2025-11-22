import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys


# Dynamically scraping the current list of NIFTY 50 components from Wikipedia source
def get_nifty_50_stocks():

    print("Attempting to dynamically scrape NIFTY 50 stock list...")
    try:
        url = 'https://en.wikipedia.org/wiki/NIFTY_50'
        
        # Using pandas.read_html to automatically parse tables from the HTML page.
        tables = pd.read_html(url)
        
        # Creating a nifty dataframe from the 2nd table on the html page
        df_nifty = tables[1]
        
        # The column name for the stock symbol is typically 'Symbol' or 'Symbol(s)'
        # Converting to list and cleaning up the symbols
        
        # Trying to find the correct column for the symbol
        symbol_col = None
        for col in df_nifty.columns:
            if 'Symbol' in col and 'Exchange' not in col:
                symbol_col = col
                break
        
        if symbol_col is None:
            raise ValueError("Could not locate the 'Symbol' column in the scraped table.")
        
        stock_list = df_nifty[symbol_col].tolist()
        
        # Using only the first 10 for efficient simulation and ensure the list is clean
        stock_list = [
            s.split(':')[0].strip().replace('.', '').upper() 
            for s in stock_list[:10] 
            if s and isinstance(s, str) and not s.startswith('INE')
        ]
        
        if not stock_list:
             raise ValueError("The scraped stock list was empty after processing.")
             
        print(f"Successfully scraped and filtered {len(stock_list)} NIFTY 50 stock symbols.")
        return stock_list

    except Exception as e:
        print(f"Warning: Dynamic scraping failed ({e}). Falling back to a current hardcoded list.")
        # Fallback list used only if scraping fails.
        return [
            'RELIANCE', 'HDFCBANK', 'TCS', 'ICICIBANK', 'INFY',
            'KOTAKBANK', 'HINDUNILVR', 'ITC', 'LT', 'SBIN'
        ]

# Generates synthetic 5-minute intraday data for a single stock. The data is mocked, but the symbols are real and dynamically sourced.
def generate_mock_intraday_data(symbol, start_time, intervals):
    data = []
    current_time = start_time
    
    # Generating a seed to ensure some stocks naturally have high correlation
    # Using the index of the stock in the list to control the correlation strength
    # (assuming the stock list is stable for the analysis script).
    stock_index = get_nifty_50_stocks().index(symbol) if symbol in get_nifty_50_stocks() else 5
    
    base_price = np.random.uniform(500, 3000)
    current_price = base_price
    current_oi = np.random.randint(100000, 500000)
    
    for _ in range(intervals):
        # 1. Simulating Price Change (Random walk, 0.1% max change)
        price_change_factor = np.random.uniform(0.999, 1.001)
        current_price *= price_change_factor
        
        # 2. Simulating OI Change based on a controlled correlation bias

        # Higher index means stronger correlation for simulation purposes
        correlation_bias = (stock_index / 10) 
        
        # Random noise for OI
        oi_base_move = np.random.normal(0, 0.003) 
        
        # Price movement influence is amplified by the correlation bias
        price_influence = (price_change_factor - 1.0) * correlation_bias * 5 
        
        oi_change_factor = 1.0 + oi_base_move + price_influence
        
        current_oi = max(int(current_oi * oi_change_factor), 50000) # Ensuring OI is non-negative
        
        data.append({
            'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'Symbol': symbol,
            'Price': round(current_price, 2),
            'Open_Interest': current_oi
        })
        current_time += timedelta(minutes=5)
        
    return data

# Main function to fetch stock list, generate mock intraday data, and save it
def fetch_data():

    NIFTY_F_AND_O_STOCKS = get_nifty_50_stocks()
    
    print("\n--- Generating Intraday Data Simulation ---")
    
    # Simulating 60 minutes of data (12 intervals) to provide plenty of data points
    INTERVALS_TO_SIMULATE = 12 
    
    start_time = datetime.now() - timedelta(minutes=INTERVALS_TO_SIMULATE * 5)
    
    all_data = []
    
    for stock in NIFTY_F_AND_O_STOCKS:
        print(f"Simulating data for {stock}...")
        stock_data = generate_mock_intraday_data(stock, start_time, INTERVALS_TO_SIMULATE)
        all_data.extend(stock_data)

    df = pd.DataFrame(all_data)
    
    output_filename = 'intraday_data.csv'
    df.to_csv(output_filename, index=False)
    
    print(f"\nSuccessfully generated {len(df)} data points and saved to '{output_filename}'.")
    
if __name__ == "__main__":
    # Required imports for scraping (pandas is already used for the analysis script)
    try:
        import requests
    except ImportError:
        print("Required library 'requests' not found. Please ensure it is installed.")
        sys.exit(1)
        
    fetch_data()