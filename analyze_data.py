import pandas as pd
import os
import sys

# Loading intraday data, calculating price and OI changes, determining correlation, and identifying the top 5 stocks with positive correlation.
def analyze_data(filename='intraday_data.csv'):
    
    if not os.path.exists(filename):
        print(f"Error: Input file '{filename}' not found.")
        print("Please run 'fetch_data.py' first to generate the necessary data.")
        sys.exit(1)

    print(f"--- Analyzing Data from '{filename}' ---")
    
    try:
        df = pd.read_csv(filename)
        # Ensuring data is sorted by Symbol and Timestamp for correct change calculation
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values(by=['Symbol', 'Timestamp'])
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}")
        sys.exit(1)

    # 1. Calculating percentage change in Price and Open Interest
    df['Price_Change_Pct'] = df.groupby('Symbol')['Price'].pct_change() * 100
    df['OI_Change_Pct'] = df.groupby('Symbol')['Open_Interest'].pct_change() * 100
    
    # Dropping the first row of each group, as pct_change() results in NaN
    df_changes = df.dropna(subset=['Price_Change_Pct', 'OI_Change_Pct']).copy()

    # Required: Calculation based on at least the last 6 data points (after change calculation)
    min_datapoints = 6
    
    # 2. Calculating the correlation coefficient for each stock
    correlation_results = {}
    
    for symbol, group in df_changes.groupby('Symbol'):
        # Ensuring enough data points for a meaningful correlation calculation
        if len(group) < min_datapoints:
            print(f"Warning: {symbol} has only {len(group)} data points. Skipping correlation.")
            continue
            
        # Calculating the correlation between Price_Change_Pct and OI_Change_Pct
        # The 'pearson' method is the standard correlation coefficient
        correlation = group['Price_Change_Pct'].corr(group['OI_Change_Pct'])
        
        # Checking for NaN correlation (happens if one of the series is constant)
        if pd.isna(correlation):
             print(f"Warning: Correlation for {symbol} is NaN (data likely constant). Skipping.")
             continue
             
        correlation_results[symbol] = correlation

    # Converting results to a DataFrame for easy sorting and filtering
    corr_df = pd.DataFrame(
        list(correlation_results.items()), 
        columns=['Symbol', 'Correlation']
    )
    
    # 3. Identifying and filtering for positive correlations
    positive_corr_df = corr_df[corr_df['Correlation'] > 0]
    
    # Sorting to find the highest positive correlations
    top_5_stocks = positive_corr_df.sort_values(by='Correlation', ascending=False).head(5)

    # 4. Displaying the results
    print("\nTop 5 Stocks with Highest Positive Intraday Price-OI Correlation:")
    print("---------------------------------------------------")

    if top_5_stocks.empty:
        print("No stocks found with a positive correlation between Price % Change and OI % Change.")
    else:
        for index, row in top_5_stocks.iterrows():
            print(f"Stock: {row['Symbol']}, Correlation: {row['Correlation']:.4f}")
            
    print("\nAnalysis complete.")

if __name__ == "__main__":
    analyze_data()