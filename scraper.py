import asyncio
import os
import logging
from datetime import datetime

logging.basicConfig(filename=os.path.normpath('log/scraper.log'), 
                    format='%(asctime)s %(message)s', 
                    level=logging.INFO)

from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email
from modules.dms import send_ping

#initalize some params
TIME_LOOP = True
time_passage = Constants.LOOP_TIME.value


"""
Main module for data scraper.
Using asyncio module to time and thread proccesses

Params:

    TIME_LOOP - boolean for controlling the while loop
    iime_passage - Time passed between every scraping
    
"""


async def cryptoConnection(delay):
    #connecting to a crypto source
    conn = Connect.crypto(
                          url=URL[1],
                          header=HEADERS['agent_desktop'], 
                          reqToSend=SEND_TO_API, 
                          send_notification=SEND_NOTIFICATION
                )
    #creating ad database in SQLLite
    cryptoConn, _ = createDb("CryptoTable")  
    conn.to_sql(f"cryptoTable_data {datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M')}", cryptoConn, if_exists='append')

    cryptoConn.close()
    #send ping to DMS after collecting
    if(ALLOW_FALLBACK):
        send_ping()
    
    #logging.info("Crypto collected")
    await asyncio.sleep(delay)


async def newsConnection(delay):
    #Connection for news scraper
    conn = Connect.news(
                        url=URL[4],
                        header=HEADERS['agent_smartphone'], 
                        reqToSend=SEND_TO_API, 
                        send_notification=SEND_NOTIFICATION
                )
    #
    #Check if date is valid
    #and select if it is
    #
    newsConn, _ = createDb("newsTable")    
    conn.to_sql(f"newsTable_data {datetime.strftime(datetime.now(), '%Y.%m.%d')}", newsConn, if_exists='append')
    newsConn.close()

    #send ping to DMS after collecting
    if(ALLOW_FALLBACK):
        send_ping()

    #logging.info("News collected")
    await asyncio.sleep(delay)

async def forexConnection(delay):

    #Forex connection
    conn = Connect.forex(
                         url=URL[6], 
                         header=HEADERS['agent_desktop'], 
                         reqToSend=SEND_TO_API, 
                         send_notification=SEND_NOTIFICATION
                )
    forexConn, _ = createDb("forexTable")  
    conn.to_sql(f"forexTable_data {datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M')}", forexConn, if_exists='append')

    forexConn.close()
    #send ping to DMS after collecting
    if(ALLOW_FALLBACK):
        send_ping()
    
    #logging.info("Forex collected")
    await asyncio.sleep(delay)

async def stockConnection(delay):
    #connecting to a crypto source
    conn = Connect.stock(
                          url=URL[9],
                          header=HEADERS['agent_desktop'], 
                          reqToSend=SEND_TO_API, 
                          send_notification=SEND_NOTIFICATION
                )
    #creating ad database in SQLLite
    stockConn, _ = createDb("StockTable")  
    conn.to_sql(f"stockTable_data {datetime.strftime(datetime.now(), '%Y.%m.%d %H:%M')}", stockConn, if_exists='append')

    stockConn.close()
    #send ping to DMS after collecting
    if(ALLOW_FALLBACK):
        send_ping()

    #logging.info("Stock collected")
    await asyncio.sleep(delay)



async def main():
    #main function to release asynchronous functions
    await cryptoConnection(time_passage)
    await newsConnection(time_passage)
    await stockConnection(time_passage)
    await forexConnection(Constants.LOOP_END_TIME.value)


if __name__=="__main__":

    while True:
        #running the whole scraper
        try:

            asyncio.run(main())

        except KeyboardInterrupt as ki:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False

            #logging.info("Progrm terminated")
            logging.info("INFO app terminated by " + ki.__name__)
            send_email(messages='Program finished', 
                    subject=str(datetime.now()), password=PASSWD)
        