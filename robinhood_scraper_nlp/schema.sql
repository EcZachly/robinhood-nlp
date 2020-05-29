CREATE TABLE robinhood.news_content(
    url TEXT,
    title TEXT,
    source TEXT,
    content TEXT,
    tickers TEXT[],
    published_at TIMESTAMP,
    updated_at TIMESTAMP,
    num_clicks INTEGER,
    cleaned_content TEXT,
    content_positive_sentiment DECIMAL,
    content_negative_sentiment DECIMAL,
    content_neutral_sentiment DECIMAL,
    title_positive_sentiment DECIMAL,
    title_negative_sentiment DECIMAL,
    title_neutral_sentiment DECIMAL
    PRIMARY KEY(url)
)