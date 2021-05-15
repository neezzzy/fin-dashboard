import requests
from datetime import datetime, timedelta
import config

'''
creates a text file with company news headlines using finnhub api
'''

symbol = 'AAPL'
days_to_subtract = 180

# YYYY-MM-DD
date_from = str((datetime.today() - timedelta(days=days_to_subtract)).strftime('%Y-%M-%d'))
date_to = '2021-05-14'

r = requests.get(f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={date_from}&to={date_to}&token={config.token}")
headlines = r.json()

with open(f"{symbol}_news.txt", 'w') as file:
    for count, headline in enumerate(headlines):
        file.write(str(count) + '. ' + headline['headline']+'\n' + headline['url'] + '\n' +
                   datetime.utcfromtimestamp(int(headline['datetime'])).strftime('%Y-%m-%d %H:%M:%S') + '\n\n')