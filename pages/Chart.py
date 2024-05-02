import streamlit as st
import yfinance as yf
import plotly.graph_objs as go

# Set up the sidebar for input
st.sidebar.header('Enter Ticker Symbol')
ticker_symbol = st.sidebar.text_input("Ticker Symbol")

# Get data on this ticker if provided, default to "AAPL" otherwise
if not ticker_symbol:
    ticker_symbol = "AAPL"

# Get data on this ticker
ticker_data = yf.Ticker(ticker_symbol)

# Get historical data for this ticker
ticker_history = ticker_data.history(period="1y")

# Calculate moving averages
ticker_history['20 Day MA'] = ticker_history['Close'].rolling(window=20).mean()
ticker_history['50 Day MA'] = ticker_history['Close'].rolling(window=50).mean()

# Calculate Bollinger Bands
ticker_history['Upper'] = ticker_history['20 Day MA'] + 2 * ticker_history['Close'].rolling(window=20).std()
ticker_history['Lower'] = ticker_history['20 Day MA'] - 2 * ticker_history['Close'].rolling(window=20).std()

# Create checkboxes for moving averages and Bollinger Bands
show_20ma = st.sidebar.checkbox("Show 20-day Moving Average", True)
show_50ma = st.sidebar.checkbox("Show 50-day Moving Average", True)
show_bands = st.sidebar.checkbox("Show Bollinger Bands", True)

# Create a candlestick chart with optional overlays
fig = go.Figure(data=[go.Candlestick(x=ticker_history.index,
                                     open=ticker_history['Open'],
                                     high=ticker_history['High'],
                                     low=ticker_history['Low'],
                                     close=ticker_history['Close'],
                                     name='Candlestick')])

if show_20ma:
    fig.add_trace(go.Scatter(x=ticker_history.index,
                             y=ticker_history['20 Day MA'],
                             mode='lines',
                             line=dict(color='blue', width=1),
                             name='20 Day MA'))

if show_50ma:
    fig.add_trace(go.Scatter(x=ticker_history.index,
                             y=ticker_history['50 Day MA'],
                             mode='lines',
                             line=dict(color='orange', width=1),
                             name='50 Day MA'))

if show_bands:
    fig.add_trace(go.Scatter(x=ticker_history.index,
                             y=ticker_history['Upper'],
                             mode='lines',
                             line=dict(color='red', width=1),
                             name='Upper Band'))
    fig.add_trace(go.Scatter(x=ticker_history.index,
                             y=ticker_history['Lower'],
                             mode='lines',
                             line=dict(color='green', width=1),
                             name='Lower Band'))

# Set chart title and axis labels
fig.update_layout(title=f"{ticker_symbol} Candlestick Chart with Moving Averages and Bollinger Bands",
                  xaxis_title='Date',
                  yaxis_title='Price')

# Display the candlestick chart with optional overlays
st.plotly_chart(fig)
