CREATE TABLE news_content(
    url TEXT,
    title TEXT,
    source TEXT,
    content TEXT,
    tickers ARRAY<TEXT>,
    published_at TIMESTAMP,
    updated_at TIMESTAMP,
    num_clicks INTEGER,
    PRIMARY KEY(url)
)