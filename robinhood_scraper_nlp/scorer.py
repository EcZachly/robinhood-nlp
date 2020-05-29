import nltk
nltk_packages = ['vader_lexicon', 'punkt']
for package in nltk_packages:
    nltk.download(package)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()


class ContentScorer:
    @classmethod
    def score(cls, input_text):
        sentiment_score = sid.polarity_scores(input_text)
        return {
            'positive_sentiment': sentiment_score['pos'],
            'negative_sentiment': sentiment_score['neg'],
            'neutral_sentiment': sentiment_score['neu']
        }
