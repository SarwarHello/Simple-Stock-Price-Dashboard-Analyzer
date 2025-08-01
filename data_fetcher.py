# import yfinance as yf
# import pandas as pd
# from datetime import datetime, timedelta # Import datetime and timedelta

# def fetch_stock_data(ticker_symbol, start_date=None, end_date=None):
#     try:
#         # Download data using yfinance
#         stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
#         if stock_data.empty:
#             print(f"No data found for {ticker_symbol} in the specified range.")
#             return pd.DataFrame() # Return empty DataFrame
        
#         stock_data.columns = [col.replace(' ', '_').lower() for col in stock_data.columns]
        
#         stock_data.index.name = 'date'
        
#         return stock_data

#     except Exception as e:
#         print(f"Error fetching data for {ticker_symbol}: {e}")
#         return pd.DataFrame() # Return empty DataFrame

# if __name__ == '__main__':
#     # Example usage:
#     apple_data = fetch_stock_data('AAPL', start_date='2023-01-01', end_date='2024-01-01')
#     if not apple_data.empty:
#         print("Apple Data (first 5 rows):")
#         print(apple_data.head())
#     today = datetime.now()
#     one_year_ago = today - timedelta(days=365) # Simple calculation for roughly one year

#     # Format dates as 'YYYY-MM-DD' strings for the function
#     start_date_str = one_year_ago.strftime('%Y-%m-%d')
#     end_date_str = today.strftime('%Y-%m-%d')

#     tesla_data = fetch_stock_data('TSLA', start_date=start_date_str, end_date=end_date_str)

#     if not tesla_data.empty:
#         print("\nTesla Data (last 5 rows):")
#         print(tesla_data.tail())

#     # Example of a non-existent ticker
#     non_existent_data = fetch_stock_data('NONEXISTENTSTOCK')







import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker_symbol, start_date=None, end_date=None, period=None):
    """
    Fetches historical stock data for a given ticker symbol.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
        start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        end_date (str, optional): End date in 'YYYY-MM-DD' format.
        period (str, optional): Valid periods: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'.
                                 If period is provided, start/end dates will be ignored.

    Returns:
        pd.DataFrame: DataFrame containing historical stock data, or an empty DataFrame if an error occurs.
    """
    try:
        raw_stock_data = None 

        if period:
            raw_stock_data = yf.download(ticker_symbol, period=period, auto_adjust=True, progress=False)
        else:
            raw_stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, auto_adjust=True, progress=False)

        # Check if it's a DataFrame and not empty
        if not isinstance(raw_stock_data, pd.DataFrame) or raw_stock_data.empty:
            print(f"yfinance download for {ticker_symbol} returned no DataFrame or an empty DataFrame.")
            return pd.DataFrame()

        stock_data = raw_stock_data.copy()

        # --- MODIFIED COLUMN RENAMING FOR MULTIINDEX ---
        # If columns are a MultiIndex (which they are for GOOGL in your case)
        if isinstance(stock_data.columns, pd.MultiIndex):
            # Option 1: Flatten by joining levels (e.g., 'Close_GOOGL')
            # new_columns = ['_'.join(col).strip().lower() for col in stock_data.columns.values]
            
            # Option 2: Extract the first level (Price metrics) and handle the 'Adj Close' specifically
            # This is often preferred for single-ticker downloads to get 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'
            new_columns = []
            for col_tuple in stock_data.columns.values:
                # The first element is the price metric (e.g., 'Close')
                # The second element is the ticker (e.g., 'GOOGL')
                if col_tuple[0] == 'Adj Close': # Handle 'Adj Close' specifically to make it 'adj_close'
                    new_columns.append('adj_close')
                else:
                    new_columns.append(col_tuple[0].replace(' ', '_').lower())
            stock_data.columns = new_columns
            
        else:
            # Original handling for single-level columns
            stock_data.columns = [col.replace(' ', '_').lower() for col in stock_data.columns]
        # --- END MODIFIED COLUMN RENAMING ---

        stock_data.index.name = 'date'
        
        # Ensure 'adj_close' column exists, which is important for subsequent calculations
        if 'adj_close' not in stock_data.columns:
            # If for some reason 'Adj Close' wasn't there, try to use 'close' as a fallback
            if 'close' in stock_data.columns:
                stock_data['adj_close'] = stock_data['close']
            else:
                print(f"Warning: Neither 'Adj Close' nor 'Close' found for {ticker_symbol}. Cannot proceed with price analysis.")
                return pd.DataFrame()


        return stock_data

    except Exception as e:
        # This catches any other unexpected errors during the process
        print(f"An unexpected error occurred for {ticker_symbol} during data fetch and processing: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    # Add an explicit test for GOOGL with a specific range
    print("\n--- Testing GOOGL ---")
    current_date = pd.to_datetime('today').strftime('%Y-%m-%d')
    googl_data = fetch_stock_data('GOOGL', start_date='2024-01-01', end_date=current_date)
    if not googl_data.empty:
        print("GOOGL Data (first 5 rows):")
        print(googl_data.head())
        print("GOOGL Columns:", googl_data.columns.tolist())
    else:
        print("Failed to fetch GOOGL data directly.")

    print("\n--- Testing AAPL (1y) ---")
    aapl_data = fetch_stock_data('AAPL', period='1y')
    if not aapl_data.empty:
        print("AAPL Data (first 5 rows from last year):")
        print(aapl_data.head())
        print("AAPL Columns:", aapl_data.columns.tolist())
    else:
        print("Failed to fetch AAPL data directly.")


    print("\n--- Testing NONEXISTENTSTOCK ---")
    non_existent_data = fetch_stock_data('NONEXISTENTSTOCK', period='1mo')
    if non_existent_data.empty:
        print("Successfully handled non-existent ticker by returning empty DataFrame.")