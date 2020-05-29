CREATE VIEW robinhood.ticker_mews_aggregates AS

SELECT UNNEST(tickers) AS ticker,
       MIN(DATE_TRUNC('day', published_at)) AS first_article_date,
       MAX(DATE_TRUNC('day', published_at)) AS last_article_date,
       AVG(title_negative_sentiment) AS avg_title_negative,
       AVG(title_neutral_sentiment) AS avg_title_neutral,
       AVG(title_positive_sentiment) AS avg_title_positive,
       AVG(title_positive_sentiment) -  AVG(title_negative_sentiment)  AS pos_negative_title_differential,
       AVG(title_positive_sentiment)/CASE WHEN AVG(title_negative_sentiment) = 0 THEN 1 ELSE AVG(title_negative_sentiment) END  AS pos_negative_title_ratio,

       AVG(content_negative_sentiment) AS avg_content_negative,
       AVG(content_neutral_sentiment) AS avg_content_neutral,
       AVG(content_positive_sentiment) AS avg_content_positive,
       AVG(content_positive_sentiment) -  AVG(content_negative_sentiment)  AS pos_negative_content_differential,
       AVG(content_positive_sentiment)/CASE WHEN AVG(content_negative_sentiment) = 0 THEN 1 ELSE AVG(content_negative_sentiment) END  AS pos_negative_content_ratio,

       COUNT(1) as num_articles,
       COUNT(CASE WHEN LENGTH(content) > 0 THEN 1 END) as num_articles_with_parsed_content

FROM robinhood.news_content
GROUP BY 1