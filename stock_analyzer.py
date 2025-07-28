import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta # Import datetime and timedelta

def fetch_stock_data(ticker_symbol, start_date=None, end_date=None):
    try:
        # Download data using yfinance
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        if stock_data.empty:
            print(f"No data found for {ticker_symbol} in the specified range.")
            return pd.DataFrame() # Return empty DataFrame
        
        stock_data.columns = [col.replace(' ', '_').lower() for col in stock_data.columns]
        
        stock_data.index.name = 'date'
        
        return stock_data

    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame() # Return empty DataFrame

if __name__ == '__main__':
    # Example usage:
    apple_data = fetch_stock_data('AAPL', start_date='2023-01-01', end_date='2024-01-01')
    if not apple_data.empty:
        print("Apple Data (first 5 rows):")
        print(apple_data.head())
    today = datetime.now()
    one_year_ago = today - timedelta(days=365) # Simple calculation for roughly one year

    # Format dates as 'YYYY-MM-DD' strings for the function
    start_date_str = one_year_ago.strftime('%Y-%m-%d')
    end_date_str = today.strftime('%Y-%m-%d')

    tesla_data = fetch_stock_data('TSLA', start_date=start_date_str, end_date=end_date_str)

    if not tesla_data.empty:
        print("\nTesla Data (last 5 rows):")
        print(tesla_data.tail())

    # Example of a non-existent ticker
    non_existent_data = fetch_stock_data('NONEXISTENTSTOCK')