import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_stock_price(df, ticker_symbol, price_column='adj_close'):
    """
    Plots the adjusted closing price of a stock over time.

    Args:
        df (pd.DataFrame): DataFrame with stock data, including a 'date' index and price column.
        ticker_symbol (str): The stock ticker symbol.
        price_column (str): The name of the column for price.
    """
    if df.empty:
        print("No data to plot for stock price.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df[price_column], label=f'{ticker_symbol} Adjusted Close Price')
    plt.title(f'{ticker_symbol} Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_daily_returns_histogram(df, ticker_symbol, returns_column='daily_returns'):
    """
    Plots a histogram of daily returns.

    Args:
        df (pd.DataFrame): DataFrame with stock data, including 'daily_returns'.
        ticker_symbol (str): The stock ticker symbol.
        returns_column (str): The name of the column for daily returns.
    """
    if df.empty or returns_column not in df.columns or df[returns_column].isnull().all():
        print("No daily returns data to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(df[returns_column].dropna(), bins=50, kde=True, color='skyblue')
    plt.title(f'Distribution of Daily Returns for {ticker_symbol}')
    plt.xlabel('Daily Return')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def plot_moving_averages(df, ticker_symbol, price_column='adj_close', short_ma_column='short_ma', long_ma_column='long_ma'):
    """
    Plots stock price along with its short and long moving averages.

    Args:
        df (pd.DataFrame): DataFrame with stock data, including price and MA columns.
        ticker_symbol (str): The stock ticker symbol.
        price_column (str): The name of the column for price.
        short_ma_column (str): The name of the column for short moving average.
        long_ma_column (str): The name of the column for long moving average.
    """
    if df.empty or short_ma_column not in df.columns or long_ma_column not in df.columns:
        print("Moving average data not available for plotting.")
        return

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df[price_column], label=f'{ticker_symbol} Adjusted Close', alpha=0.7)
    plt.plot(df.index, df[short_ma_column], label=f'{short_ma_column.replace("_", " ").title()}', color='orange')
    plt.plot(df.index, df[long_ma_column], label=f'{long_ma_column.replace("_", " ").title()}', color='green')
    plt.title(f'{ticker_symbol} Stock Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    # Example usage (requires data_fetcher.py and data_processor.py)
    from data_fetcher import fetch_stock_data
    from data_processor import calculate_metrics

    # Fetch and process data
    aapl_data = fetch_stock_data('AAPL', start_date='2023-01-01')
    processed_aapl_data = calculate_metrics(aapl_data)

    if not processed_aapl_data.empty:
        # Plotting examples
        print("Generating plots...")
        plot_stock_price(processed_aapl_data, 'AAPL')
        plot_daily_returns_histogram(processed_aapl_data, 'AAPL')
        plot_moving_averages(processed_aapl_data, 'AAPL')
        print("Plots generated. Check your display.")