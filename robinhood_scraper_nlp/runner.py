import os
import psycopg2
import csv

from robinhood_scraper_nlp.parser import BloombergParser, MarketWatchParser, RobinhoodParser, GoogleNewsParser, YahooFinancialParser, CNBCParser, ReutersParser, BenzingaParser
from pyrh import Robinhood

DEFAULT_TICKERS = ["FB", "AAPL", "AMZN", "NFLX", "GOOGL",
                   "AMD", "TSM", "INTC", "NVDA",
                   "AMZN", "MSFT", "TSLA", "UBER", "CGC",
                   "LYFT", "SNAP", "AAPL", "CRM", "ACB",
                   "CRON", "APHA", "FIT", "GPRO", "SNAP", "TWTR"]


class ScraperRunner:

    @classmethod
    def run_scraper(cls,
                    tickers=None,
                    mode="csv",
                    output_directory="output",
                    output_filename="output_data.csv",
                    database_user=None,
                    database_host=None,
                    database_password=None,
                    database_name=None,
                    database_schema=None
        ):

        if not tickers:
            tickers = DEFAULT_TICKERS

        robinhood = ScraperRunner.login_to_robinhood()

        parsed_content = []
        for t in tickers:
            content = ScraperRunner.get_content_for_stock(t, robinhood)
            if content:
                parsed_content.extend(content)
        parsed_content.sort(key=lambda val: val.url)
        if mode == 'csv':
            ScraperRunner.write_to_csv(parsed_content, output_directory, output_filename)
        elif mode == 'database':
            ScraperRunner.write_to_database(parsed_content, database_host, database_name, database_user, database_password, database_schema)

    @classmethod
    def write_to_database(cls, parsed_content, host, database_name, username, password, schema, table_name="news_content"):
        conn_string = "host={host} dbname={database_name} user={username} password={password} sslmode=require".format(
            host=host,
            database_name=database_name,
            username=username,
            password=password
        )
        full_table_name = '{schema}.{table_name}'.format(schema=schema, table_name=table_name)
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()
        for content in parsed_content:
            try:
                query = """
                    INSERT INTO {full_table_name} 
                                  (url, title, source, content, tickers, 
                                    num_clicks, published_at, updated_at, cleaned_content,
                                    content_positive_sentiment, content_negative_sentiment, content_neutral_sentiment,
                                    title_positive_sentiment, title_negative_sentiment, title_neutral_sentiment
                                  ) 
                                  VALUES('{url}', '{title}', '{source}', '{content}', ARRAY{tickers}::TEXT[], {num_clicks}, '{published_at}', '{updated_at}', 
                                        '{cleaned_content}', {content_positive_sentiment}, {content_negative_sentiment}, {content_neutral_sentiment}, 
                                          {title_positive_sentiment}, {title_negative_sentiment}, {title_neutral_sentiment}   )
                                  ON CONFLICT (url)                            
                                  DO UPDATE
	                              SET content = EXCLUDED.content, 
	                                  tickers = EXCLUDED.tickers,
	                                  cleaned_content = EXCLUDED.cleaned_content,
	                                  num_clicks=EXCLUDED.num_clicks, 
	                                  updated_at=EXCLUDED.updated_at,
	                                  content_positive_sentiment=EXCLUDED.content_positive_sentiment,
	                                  content_negative_sentiment=EXCLUDED.content_negative_sentiment,
	                                  content_neutral_sentiment=EXCLUDED.content_neutral_sentiment,
	                                  title_positive_sentiment=EXCLUDED.title_positive_sentiment,
	                                  title_negative_sentiment=EXCLUDED.title_negative_sentiment,
	                                  title_neutral_sentiment=EXCLUDED.title_neutral_sentiment
	                              ;
                    """.format(
                    full_table_name=full_table_name,
                    url=content.url,
                    source=content.source,
                    title=content.title.replace("'", "''").replace('"', '""'),
                    content=content.content.replace("'", "''").replace('"', '""'),
                    cleaned_content=content.cleaned_content,
                    tickers=content.tickers,
                    num_clicks=content.num_clicks,
                    published_at=content.published_at,
                    updated_at=content.updated_at,
                    content_positive_sentiment=content.scores['positive_sentiment'],
                    content_negative_sentiment=content.scores['negative_sentiment'],
                    content_neutral_sentiment=content.scores['neutral_sentiment'],
                    title_positive_sentiment=content.title_scores['positive_sentiment'],
                    title_negative_sentiment=content.title_scores['negative_sentiment'],
                    title_neutral_sentiment=content.title_scores['neutral_sentiment']
                )
                cursor.execute(query)
                connection.commit()
            except Exception as e:
                print(e)

    @classmethod
    def login_to_robinhood(cls):
        PASSWORD = os.environ.get('ROBINHOOD_PASSWORD')  # your Robinhood password
        EMAIL = os.environ.get('ROBINHOOD_EMAIL')  # your Robinhood email
        QR_CODE = os.environ.get('ROBINHOOD_QR_CODE')  # your Robinhood QR Code

        if not EMAIL:
            EMAIL = input("What is your Robinhood email?").strip()

        if not PASSWORD:
            PASSWORD = input("What is your Robinhood password?").strip()

        if not QR_CODE:
            QR_CODE = input("What is your Robinhood QR code?").strip()

        robinhood = Robinhood()
        robinhood.login(username=EMAIL, password=PASSWORD, qr_code=QR_CODE)
        return robinhood


    @classmethod
    def write_to_csv(cls, parsed_content, output_directory, output_filename):
        try:
            os.mkdir(output_directory)
        except Exception:
            print('-----')
        output_filepath = os.path.join(output_directory, output_filename)
        with open(output_filepath, newline='\n', encoding='utf-8',
                  mode='w') as csv_file:
            for content in parsed_content:
                writer = csv.writer(csv_file)
                writer.writerow([content.url, content.tickers, content.num_clicks,
                                 content.published_at, content.updated_at, content.source,
                                 content.title, content.content])


    @classmethod
    def get_content_for_stock(cls, ticker, robinhood):
        data = robinhood.get_news(ticker)
        results = data['results']
        fetched_results = []
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
            data = None
            if source in switch_block:
                p = switch_block[source](url, result)
                data = p.parse()
                if ticker not in data.tickers:
                    data.tickers.append(ticker)
            else:
                print("No parser found for url:" + url)
            if data is not None:
                fetched_results.append(data)
        return fetched_results


if __name__ == '__main__':
    PASSWORD = os.environ.get("RESULTS_DATABASE_PASSWORD")
    USERNAME = os.environ.get("RESULTS_DATABASE_USERNAME")
    HOST = os.environ.get("RESULTS_DATABASE_HOST")
    DATABASE_NAME = os.environ.get("RESULTS_DATABASE_NAME")
    ScraperRunner.run_scraper(mode="database",
                              database_name=DATABASE_NAME,
                              database_password=PASSWORD,
                              database_user=USERNAME,
                              database_host=HOST,
                              database_schema="robinhood")