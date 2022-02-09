import streamlit as st
import pandas as pd
import requests
import json
import csv
from datetime import datetime, timezone
import plotly.graph_objects as go
import config


# application dashboard using finnhub api and streamlit
st.header('Welcome to Financial Dashboard')

st.sidebar.title('Options')
option = st.sidebar.selectbox(
    'Which Dashboard?', ('Company News', 'Company Profile', 'Insider Transactions'))
st.title(option)

if option == 'Insider Transactions':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    r = requests.get(
        f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={config.token}")
    data = r.json()
    st.header(f"Insider selling for {symbol}")

    if len(data['data']) > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Name")
            for insider in data['data']:
                st.write(insider['name'])
        with col2:
            st.header("Shares")
            for insider in data['data']:
                st.write(insider['share'])
        with col3:
            st.header("Date")
            for insider in data['data']:
                st.write(insider['filingDate'])
        with col4:
            st.header("Price")
            for insider in data['data']:
                st.write(f'$ {insider["transactionPrice"]}')
    else:
        st.subheader('No insider activity.')

if option == 'Company News':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    r = requests.get(
        f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2021-03-01&to=2021-03-09&token={config.token}")
    data = r.json()
    for news_item in data:
        st.write(news_item['source'])
        # st.image(news_item['image'])
        st.subheader(news_item['headline'])
        st.write(datetime.utcfromtimestamp(
            int(news_item['datetime'])).strftime('%Y-%m-%d %H:%M:%S'))
        st.write(news_item['url'])

if option == 'Company Profile':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    r = requests.get(
        f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={config.token}")
    stock = r.json()
    st.write(stock['name'])
    st.image(stock['logo'])
    st.image(f"https://finviz.com/chart.ashx?t={symbol}")
    st.write("IPO date: " + str(stock['ipo']))
    st.write("Country of company's headquarter: " + str(stock['country']))
    st.write("Market Capitalization: " + str(stock['marketCapitalization']))
    st.write("Number of oustanding shares: " + str(stock['shareOutstanding']))
