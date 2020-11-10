## Crypto , Forex, News scraper
# Scraper tha will run in asynchronous matter to store data in SQLite
# DB files will be stored in saved folder


# Scraper.py - main module for data scraper.
Using asyncio module to time and thread proccesses

Params:

    TIME_LOOP - boolean for controlling the while loop
    iime_passage - Time passed between every scraping

# dp.py - database module for scraper . Using SQLAlchemy

# smtp.py - Module for email logging

send_email() - email sending main function

Params:

    messages - message body to send
    subject - subject of the emal
    password - password for the SMTP server

# apiRequests.py - module for sending scraped data to Serverside API

sendPost() - Send scraped data to api
getPost() - get scraped data from API

Params:

    url - default None , no implementation . Removing soon
    apiloc - IP or URL of API
    data - datasource to send to API

# dataCollector.py - module for connecting diffrent connection elements together

forex() - for scraping forex data
crypto()  - for scraping crypto data
news()  -  for scraping news data

params: 

    url - passing right URL from connection.var
    header - header to send with a requests

for news source:

    reqToSend - a boolean for sending data to API

Will implement preciOus metal quote scraper in a later release