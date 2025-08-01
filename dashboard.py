import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Import your custom modules
from data_fetcher import fetch_stock_data
from data_processor import calculate_metrics

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="Simple Stock Analyzer")

st.title("📈 Simple Stock Price Dashboard")
st.markdown("Explore historical stock data, daily returns, and moving averages.")

# --- Sidebar for User Input ---
st.sidebar.header("User Input")

ticker_symbol = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)", value="GOOGL").upper()

# Date range selection
today = pd.to_datetime('today').date()
default_start_date = pd.to_datetime('2023-01-01').date() # Default to start of last year
default_end_date = today

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(default_start_date, default_end_date),
    min_value=pd.to_datetime('2000-01-01').date(), # Adjust min historical date as needed
    max_value=today
)

# Ensure date_range is not empty and has two elements
if len(date_range) == 2:
    start_date = date_range[0].strftime('%Y-%m-%d')
    end_date = date_range[1].strftime('%Y-%m-%d')
else:
    st.sidebar.warning("Please select a valid start and end date.")
    st.stop() # Stop execution if date range is incomplete

short_ma_window = st.sidebar.slider("Short Moving Average Window (days)", min_value=10, max_value=50, value=20)
long_ma_window = st.sidebar.slider("Long Moving Average Window (days)", min_value=50, max_value=200, value=100)

# --- Fetch and Process Data ---
if ticker_symbol:
    st.subheader(f"Analyzing: {ticker_symbol}")

    with st.spinner(f"Fetching data for {ticker_symbol}..."):
        stock_data = fetch_stock_data(ticker_symbol, start_date=start_date, end_date=end_date)

    if not stock_data.empty:
        processed_data = calculate_metrics(stock_data, short_ma_window=short_ma_window, long_ma_window=long_ma_window)

        # --- Display Raw Data (Optional) ---
        if st.sidebar.checkbox("Show Raw Data"):
            st.subheader("Raw Data (First 10 Rows)")
            st.dataframe(stock_data.head(10))

        # --- Visualizations ---
        st.subheader(f"{ticker_symbol} Stock Price and Moving Averages")

        # Plotly for interactive charts
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=processed_data.index, y=processed_data['adj_close'], mode='lines', name='Adjusted Close'))
        fig_price.add_trace(go.Scatter(x=processed_data.index, y=processed_data['short_ma'], mode='lines', name=f'{short_ma_window}-Day MA', line=dict(color='orange')))
        fig_price.add_trace(go.Scatter(x=processed_data.index, y=processed_data['long_ma'], mode='lines', name=f'{long_ma_window}-Day MA', line=dict(color='green')))
        
        fig_price.update_layout(
            title=f'{ticker_symbol} Stock Price with Moving Averages',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig_price, use_container_width=True)

        st.subheader(f"Daily Returns for {ticker_symbol}")
        # Histogram for daily returns
        fig_returns = px.histogram(
            processed_data.dropna(subset=['daily_returns']), # Drop NaN for plotting
            x='daily_returns',
            nbins=50,
            title=f'Distribution of Daily Returns for {ticker_symbol}',
            labels={'daily_returns': 'Daily Return'},
            height=400
        )
        fig_returns.update_layout(bargap=0.1)
        st.plotly_chart(fig_returns, use_container_width=True)

        # --- Key Metrics ---
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)

        latest_price = processed_data['adj_close'].iloc[-1]
        col1.metric("Latest Close Price", f"${latest_price:,.2f}")

        # Calculate latest daily return, handling NaN
        latest_daily_return = processed_data['daily_returns'].iloc[-1] * 100 if not processed_data['daily_returns'].isnull().iloc[-1] else 0.0
        col2.metric("Latest Daily Return", f"{latest_daily_return:,.2f}%", delta=f"{latest_daily_return:,.2f}%")

        # Simple volatility (standard deviation of daily returns)
        volatility = processed_data['daily_returns'].std() * 100
        col3.metric("Daily Volatility (Std Dev of Returns)", f"{volatility:,.2f}%")

    else:
        st.error(f"Could not retrieve data for ticker symbol: {ticker_symbol}. Please check the symbol and try again.")
else:
    st.info("Please enter a stock ticker symbol in the sidebar to get started.")