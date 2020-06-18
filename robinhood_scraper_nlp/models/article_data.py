from robinhood_scraper_nlp.utils.cleaner import ContentCleaner
from robinhood_scraper_nlp.utils.scorer import ContentScorer

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

    @property
    def cleaned_title(self):
        return ContentCleaner.clean_text(self.title)

    @property
    def title_scores(self):
        return ContentScorer.score(self.cleaned_title)

    @property
    def cleaned_content(self):
        return ContentCleaner.clean_text(self.content)

    @property
    def scores(self):
        return  ContentScorer.score(self.cleaned_content)

