import streamlit as st
import pandas as pd
import yfinance as yf
from babel.numbers import format_currency

# Function to format currency, to get it straight
def format_price(price):
    if price is not None:
        return format_currency(price, 'USD', locale='en_US')  # Format price in USD with two decimals
    else:
        return None

# Function to calculate percentage change
def calculate_percentage_change(data, period):
    if data is not None and len(data) >= period:
        start_price = data.iloc[0]['Close']
        end_price = data.iloc[-1]['Close']
        return round(((end_price - start_price) / start_price) * 100, 1)  # Round to one decimal place
    else:
        return None

# Function to get stock data
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist_data = stock.history(period="5y")
        
        current_price = format_price(hist_data.iloc[-1]['Close'])
        three_day_change_pct = calculate_percentage_change(hist_data.tail(3), 3)
        seven_day_change_pct = calculate_percentage_change(hist_data.tail(7), 7)
        thirty_day_change_pct = calculate_percentage_change(hist_data.tail(30), 30)
        ninety_day_change_pct = calculate_percentage_change(hist_data.tail(90), 90)
        one_eighty_day_change_pct = calculate_percentage_change(hist_data.tail(180), 180)
        one_year_change_pct = calculate_percentage_change(hist_data.tail(252), 252)  # Assuming 252 trading days in a year
        five_year_change_pct = calculate_percentage_change(hist_data, len(hist_data))
        
        return {
            'Ticker': ticker,
            'Price': current_price,
            '3-d': f"{three_day_change_pct}%",
            '7-d': f"{seven_day_change_pct}%",
            '30-d': f"{thirty_day_change_pct}%",
            '90-d': f"{ninety_day_change_pct}%",
            '180-d': f"{one_eighty_day_change_pct}%",
            '1-yr': f"{one_year_change_pct}%",
            '5-yr': f"{five_year_change_pct}%"
        }
    except Exception as e:
        st.warning(f"Failed to fetch data for {ticker}: {str(e)}")
        return {
            'Ticker': ticker,
            'Price': None,
            '3-d': None,
            '7-d': None,
            '30-d': None,
            '90-d': None,
            '180-d': None,
            '1-yr': None,
            '5-yr': None
        }

# List of stocks and tickers
stocks = {
    'ADR ON CEMEX S.A.B DE C.V.': 'CX',
    'ADR ON COMPAÑÍA CERVECERÍAS UNIDAS': 'CCU',
    'ADR ON PETRÓLEO BRASILEIRO S.A.-': 'PBR',
    'ADR ON RIO TINTO PLC': 'RIO',
    'ADR ON SOCIEDAD QUIMICA Y MINERA': 'SQM',
    'ADR ON VALE': 'VALE',
    'ALIBABA GROUP HOLDING LTD': 'BABA',
    'AT&T INC.': 'T',
    'CANADIAN NATIONAL RAIL': 'CNI',
    'FRANKLIN FTSE CHINA UCITS ETF': 'FLCH',
    'INTEL CORPORATION': 'INTC',
    'KAZATOMPROM  GDR REGS 1/1': 'KAP.IL',
    'LIBERTY MEDIA A SIRIUSXM': 'LSXMA',
    'LUMEN TECHNOLOGIES': 'LUMN',
    'MICROSOFT CORPORATION': 'MSFT',
    'NEW FOUND GOLD CORP COMMON SHARES': 'NFG.V',
    'OCI': 'OCI.AS',
    'PROSUS': 'PRX.AS',
    'TAKEAWAY': 'TKWY.AS',
    'VANECK JUNIOR GOLD MINERS UCITS ETF': 'GDXJ',
    'ZIM INTEGRATED SHIPPING SERVICES': 'ZIM',
    'SOCIEDAD QUIMICA Y MINERA': 'SQM',  # Adding SQM to the list
    'PPL': 'PPL',
    'AEM': 'AEM',
    'DV.V': 'DV.V',
    'DG': 'DG'
}

# Create a table to display stock data
st.write("## Portfolio")
table_data = []
for stock_name, ticker in stocks.items():
    stock_data = get_stock_data(ticker)
    if stock_data:
        table_data.append(stock_data)

# Create DataFrame
df = pd.DataFrame(table_data)

# Style DataFrame to change font color for negative numbers to red
styled_df = df.style.applymap(lambda x: 'color: red' if isinstance(x, str) and '-' in x else '')

# Display styled DataFrame
st.write(styled_df)

# Create another table for the specified tickers
st.write("## Watchlist")
additional_stocks = {
    'PPL': 'PPL',
    'AEM': 'AEM',
    'DV.V': 'DV.V',
    'DG': 'DG'
}

table_data_additional = []
for stock_name, ticker in additional_stocks.items():
    stock_data = get_stock_data(ticker)
    if stock_data:
        table_data_additional.append(stock_data)

# Create DataFrame for additional stocks
df_additional = pd.DataFrame(table_data_additional)

# Style DataFrame to change font color for negative numbers to red
styled_df_additional = df_additional.style.applymap(lambda x: 'color: red' if isinstance(x, str) and '-' in x else '')

# Display styled DataFrame for additional stocks
st.write(styled_df_additional)
