import asyncio
import logging
from datetime import datetime
import os

#Log file location
logging.basicConfig(filename=os.path.normpath('log/scraper.log'))

import pandas as pd

from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email
from modules.dms import send_ping

#initalize some params
TIME_LOOP = True
time_passage = Constants.LOOP_TIME.value
_ALLOW_FALLBACK = True

"""
Main module for data scraper.
Using asyncio module to time and thread proccesses

Params:

    TIME_LOOP - boolean for controlling the while loop
    iime_passage - Time passed between every scraping
    
"""


async def cryptoConnection(delay):
    #connecting to a crypto source
    conn = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
    #creating ad database in SQLLite
    cryptoConn, dbName = createDb("CryptoTable")  
    conn.to_sql(dbName, cryptoConn, if_exists='append')

    logging.info("Crypto collected")
    cryptoConn.close()
    #send ping to DMS after collecting
    if(_ALLOW_FALLBACK):
        send_ping()

    await asyncio.sleep(delay)


async def newsConnection(delay):
    #Connection for news scraper
    conn = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'], reqToSend=True, send_notification=False)
    newsConn, dbName = createDb("newsTable")  
    conn.to_sql(dbName, newsConn, if_exists='append')

    logging.info("News collected")
    newsConn.close()
    #send ping to DMS after collecting
    if(_ALLOW_FALLBACK):
        send_ping()

    await asyncio.sleep(delay)

async def forexConnection(delay):

    #Forex connection
    conn = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'], reqToSend=True, send_notification=False)
    forexConn, dbName = createDb("forexTable")  
    conn.to_sql(dbName, forexConn, if_exists='append')

    logging.info("Forex collected")
    forexConn.close()
    #send ping to DMS after collecting
    if(_ALLOW_FALLBACK):
        send_ping()

    await asyncio.sleep(delay)

async def main():
    #main function to release asynchronous functions
    await cryptoConnection(time_passage)
    await newsConnection(time_passage)
    await forexConnection(Constants.LOOP_END_TIME.value)


if __name__=="__main__":

    while True:
        #running the whole scraper
        try:

            asyncio.run(main())

        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False

            logging.info(f"{str(datetime.now())} Progrm terminated")

            send_email(messages='Program finished', 
                    subject=str(datetime.now()), password=PASSWD)
        