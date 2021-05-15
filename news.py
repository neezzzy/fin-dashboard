import requests
from datetime import datetime
import config

'''
creates a text file with crypto news headlines using finnhub api
'''


news_query = 'crypto'
r = requests.get(
    f"https://finnhub.io/api/v1/news?category={news_query}&token={config.token}")
headlines = r.json()


with open(f"{news_query}_news.txt", 'w') as file:
    for count, headline in enumerate(headlines):
        file.write(str(count) + '. ' + headline['headline']+'\n' + headline['url'] + '\n' +
                   datetime.utcfromtimestamp(int(headline['datetime'])).strftime('%Y-%m-%d %H:%M:%S') + '\n\n')
        # print(headline['headline'] + '\n')
