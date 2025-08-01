import pandas as pd
import numpy as np

def calculate_metrics(df, price_column='adj_close', short_ma_window=20, long_ma_window=50):
    """
    Calculates daily returns and moving averages for stock data.

    Args:
        df (pd.DataFrame): DataFrame with stock data, including a 'date' index
                           and 'adj_close' (or specified price_column).
        price_column (str): The name of the column to use for price calculations.
        short_ma_window (int): Window for the short-term moving average.
        long_ma_window (int): Window for the long-term moving average.

    Returns:
        pd.DataFrame: DataFrame with added 'daily_returns', 'short_ma', and 'long_ma' columns.
                      Returns empty DataFrame if input is empty.
    """
    if df.empty:
        return pd.DataFrame()

    df_copy = df.copy() # Work on a copy to avoid modifying original DataFrame

    # 1. Calculate Daily Returns
    # Formula: (Current Price - Previous Price) / Previous Price
    # .pct_change() is a convenient pandas method for this
    df_copy['daily_returns'] = df_copy[price_column].pct_change()

    # 2. Calculate Moving Averages (Simple Moving Average - SMA)
    # The 'rolling' method is used to apply a moving window calculation.
    df_copy['short_ma'] = df_copy[price_column].rolling(window=short_ma_window).mean()
    df_copy['long_ma'] = df_copy[price_column].rolling(window=long_ma_window).mean()

    # Drop any rows with NaN values introduced by calculations (e.g., first few rows for MA)
    # Or, you can choose to keep them and handle them in visualization.
    # For simplicity, let's keep them as NaN values for now, so the dates align.

    return df_copy

if __name__ == '__main__':
    # Example usage (requires data_fetcher.py)
    from data_fetcher import fetch_stock_data

    # Fetch some data
    msft_data = fetch_stock_data('MSFT', start_date='2023-01-01', end_date='2024-07-01')

    if not msft_data.empty:
        # Calculate metrics
        processed_msft_data = calculate_metrics(msft_data)
        print("Microsoft Data with Metrics (last 10 rows):")
        print(processed_msft_data.tail(10))

        # Check for NaN values at the start due to moving average calculation
        print("\nNaN values due to MA calculation at the start:")
        print(processed_msft_data[['adj_close', 'daily_returns', 'short_ma', 'long_ma']].head(60))