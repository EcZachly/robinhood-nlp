import os
import requests
from parser import NewsParser, BloombergParser, MarketWatchParser, RobinhoodParser, GoogleNewsParser, YahooFinancialParser, CNBCParser, ReutersParser, BenzingaParser
from pyrh import Robinhood

PASSWORD = os.environ.get('ROBINHOOD_PASSWORD')
EMAIL = os.environ.get('ROBINHOOD_EMAIL')
QR_CODE = os.environ.get('ROBINHOOD_QR_CODE')
rh = Robinhood()
rh.login(username=EMAIL, password=PASSWORD, qr_code=QR_CODE)


def get_content_for_stock(ticker):
    data = rh.get_news(ticker)
    results = data['results']
    for result in results:
        url = result['url']
        source = result['api_source'].lower()
        print('Fetching data for url: ' + url)
        switch_block = {
            'marketwatch': MarketWatchParser,
            'yahoo': YahooFinancialParser,
            'cnbc': CNBCParser,
            'reuters': ReutersParser,
            'benzinga': BenzingaParser,
            'google': GoogleNewsParser,
            'robinhood': RobinhoodParser,
            'bloomberg': BloombergParser
        }
        if source in switch_block:
            p = switch_block[source](url, result)
            data = p.parse()
            data.write_to_csv("outputdata.csv")
        else:
            print("No parser found for url:" + url)


tickers = ["NFLX", "FB", "FIT",
           "GOOGL", "AMZN", "MSFT",
           "TSLA", "UBER", "CGC",
           "LYFT", "SNAP", "AAPL", "CRM"]

for t in tickers:
    get_content_for_stock(t)