import string
import requests
from robinhood_scraper_nlp.cleaner import ContentCleaner
from robinhood_scraper_nlp.scorer import ContentScorer
from bs4 import BeautifulSoup


class NewsArticleData:
    def __init__(self, content, tickers, api_result):
        self.content = content
        self.tickers = tickers
        self.url = api_result['url']
        self.num_clicks = api_result['num_clicks']
        self.published_at = api_result['published_at']
        self.updated_at = api_result['updated_at']
        self.title = api_result['title']
        self.source = api_result['source']
        self.cleaned_content = ContentCleaner.clean_text(content)
        self.cleaned_title = ContentCleaner.clean_text(self.title)
        self.scores = ContentScorer.score(self.cleaned_content)
        self.title_scores = ContentScorer.score(self.cleaned_title)


def remove_punctuation(line):
    return line.translate(str.maketrans('', '', string.punctuation))


class StockSymbol:
    def __init__(self, ticker, change):
        self.ticker = ticker
        self.change = change


class NewsParser:
    def __init__(self, url, api_result):
        self.url = url
        self.api_result = api_result

    def parse(self):
        raise NotImplementedError('Please use a sub class not this one')


class MarketWatchParser(NewsParser):
    def parse(self):
        if 'yahoo' not in self.url:
            try:
                response = requests.get(self.url)
                response.raise_for_status()
            except Exception:
                print('Error getting url')
                return
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            tickers = soup.find_all(attrs={'class': 'qt-chip'})
            mentioned_tickers = []
            for stock in tickers:
                stock_text = stock.text.split(',')
                symbol = StockSymbol(ticker=stock_text[0].strip(), change=stock_text[1].strip())
                mentioned_tickers.append(symbol)
            content = soup.find_all(attrs={'class': 'article__content'})[0].text.strip()
            content_rows = content.split('\n')
            filtered_content_rows = []
            mentioned_tickers_symbols = list(map(lambda s: s.ticker, mentioned_tickers))
            mentioned_tickers_changes = list(map(lambda s: s.change, mentioned_tickers))
            for row in content_rows:
                if len(row.strip()) > 0:
                    row = row.strip()
                    contains_change = row in mentioned_tickers_changes
                    stripped_row = remove_punctuation(row).strip()
                    contains_ticker = stripped_row in mentioned_tickers_symbols
                    if not contains_change and not contains_ticker:
                        filtered_content_rows.append(row)
            filtered_content = ' '.join(filtered_content_rows)
            return NewsArticleData(content=filtered_content, tickers=mentioned_tickers_symbols, api_result=self.api_result)
        else:
            return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class BloombergParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class YahooFinancialParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class CNBCParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class ReutersParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class BenzingaParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class RobinhoodParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)


class GoogleNewsParser(NewsParser):
    def parse(self):
        return NewsArticleData(content="", tickers=[], api_result=self.api_result)

