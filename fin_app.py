import streamlit as st
import pandas as pd
import requests, json, csv
from datetime import datetime, timezone
import plotly.graph_objects as go
import config

'''
application dashboard using finnhub api and streamlit
'''

st.sidebar.title('Options')
option = st.sidebar.selectbox(
    'Which Dashboard?', ('Company News', 'Company Profile', 'News Sentiment', 'Insider Transactions', 'Chart'))
st.title(option)

if option == 'Insider Transactions':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    r = requests.get(
        f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={symbol}&token={config.token}")
    data = r.json()
    st.header(f"Insider selling for {symbol}")
    if len(data['data']) > 0:
        for insider in data['data']:
            st.write(insider['name'])
            st.write(insider['share'])
            st.write(insider['filingDate'])
            st.write(insider['transactionPrice'])
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

if option == 'News Sentiment':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    st.header(f"{symbol} News Sentiment")
    r = requests.get(
        f"https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={config.token}")
    stock = r.json()

    st.write("Statistics of company news in the past week: " +
             str(stock['buzz']['buzz']))
    st.write("News score: " + str(stock['companyNewsScore']))
    st.image(f"https://finviz.com/chart.ashx?t={symbol}")
    st.write("Sector average bullish percent: " +
             str(stock['sectorAverageBullishPercent']))
    st.write("Sector average bearish percent: " +
             str(stock['sentiment']['bearishPercent']))
    st.write("Sector average bullish percent: " +
             str(stock['sentiment']['bullishPercent']))

if option == 'Chart':
    symbol = st.sidebar.text_input('Symbol', value='AAPL', max_chars=5)
    st.header(f"{symbol} Candlestick Chart")
  
    from_date = st.sidebar.slider("From what date",
      value=datetime(2021, 1, 1),
      format="MM/DD/YY")
    
    to_date = st.sidebar.slider("To what date",
      value=datetime(2021, 1, 1),
      format="MM/DD/YY")
  
    from_date_unix = int((from_date - datetime(1970, 1, 1)).total_seconds())
    to_date_unix = int((to_date - datetime(1970, 1, 1)).total_seconds())
    
    st.write(from_date_unix)
    st.write(to_date_unix)
    
    options = ['5', '15', '30', '60', 'D', 'W', 'M']
    resolution = st.sidebar.radio('timeframe', options, index=3)
        
    r = requests.get(
        f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution={resolution}&from={from_date_unix}&to={to_date_unix}&token={config.token}")
    data = r.json()
    # st.write(data)

    
    df = pd.DataFrame(data)
    # st.write(df)
    fig = go.Figure(data=[go.Candlestick(x=pd.to_datetime(df['t'],unit='s'),
                    open=df['o'],
                    high=df['h'],
                    low=df['l'],
                    close=df['c'])])
    fig.layout.xaxis.type = 'category'
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    st.write(df)
    
        
    
