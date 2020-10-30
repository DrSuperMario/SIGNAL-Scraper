from sqlalchemy import create_engine

engineCrypto = create_engine('sqlite:///saved/crypto_data.db', echo=True)
sqlite_conn1 = engineCrypto.connect()

sqliteTableCrypto = 'Scraped Crypto Data'

engineForex = create_engine('sqlite:///saved/forex_data.db', echo=True)
sqlite_conn2 = engineForex.connect()

sqliteTableForex = 'Scraped Forex Data'

engineNews = create_engine('sqlite:///saved/news_data.db', echo=True)
sqlite_conn3 = engineNews.connect()

sqliteTableNews = 'Scraped News Data'
