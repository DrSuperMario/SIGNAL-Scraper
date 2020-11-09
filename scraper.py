import asyncio
import logging
from datetime import datetime
import os

logging.basicConfig(filename=os.path.normpath('log/scraper.log'))

import pandas as pd

from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email


TIME_LOOP = True
time_passage = Constants.LOOP_TIME.value


async def cryptoConnection(delay):

    conn = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])

    cryptoConn, dbName = createDb("CryptoTable")  
    conn.to_sql(dbName, cryptoConn, if_exists='append')
    try:

        send_email(messages='Information Collected from Crypto Source',
                     subject=str(datetime.now()), password=PASSWD)
    
    except EnvironmentError:
        logging.error(f"{str(datetime.now())}Mail not sent , error 40000 from CryptoConnectionr")
        print("Error occured with SMTP authentication")

    logging.info("Crypto collected")
    cryptoConn.close()
    await asyncio.sleep(delay)


async def newsConnection(delay):

    conn = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'], reqToSend=True)
    newsConn, dbName = createDb("newsTable")  
    conn.to_sql(dbName, newsConn, if_exists='append')
    try:

        send_email(messages='Information Collected from News sources', 
                    subject=str(datetime.now()), password=PASSWD)

    except EnvironmentError:
        logging.error(f"{str(datetime.now())} Mail not sent , error 40000 from newsConnection")
        print("Error occured with SMTP authentication")

    logging.info("News collected")
    newsConn.close()
    await asyncio.sleep(delay)

async def forexConnection(delay):

    #Forex connection
    conn = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])
    forexConn, dbName = createDb("forexTable")  
    conn.to_sql(dbName, forexConn, if_exists='append')
    try:

        send_email(messages='Information Collected from Forex sources', 
                    subject=str(datetime.now()), password=PASSWD)

    except EnvironmentError:
        logging.error(f"{str(datetime.now())} Mail not sent , error 40000 from ForexConnection")
        print("Error occured with SMTP authentication")

    logging.info("Forex collected")
    forexConn.close()
    await asyncio.sleep(delay)

async def main():

    await cryptoConnection(time_passage)
    await newsConnection(time_passage)
    await forexConnection(Constants.LOOP_END_TIME.value)


if __name__=="__main__":

    while True:

        try:

            asyncio.run(main())

        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False

            logging.info(f"{str(datetime.now())} Progrm terminated")

            send_email(messages='Program finished', 
                    subject=str(datetime.now()), password=PASSWD)
        