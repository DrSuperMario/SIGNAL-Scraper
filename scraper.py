import asyncio
import smtplib
import logging
from datetime import datetime
import os

import pandas as pd

from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email


TIME_LOOP = True
time_passage = 1
date_as = str(datetime.now())
logging.basicConfig(filename=os.path.normpath('log/scraper.log.log'))

async def cryptoConnection(delay):

    conn = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])

    cryptoConn, dbName = createDb("CryptoTable")  
    conn.to_sql(dbName, cryptoConn, if_exists='append')
    try:

        send_email(messages='Information Collected from Crypto Source',
                     subject=date_as, password=PASSWD)
    
    except EnvironmentError:
        logging.error("Mail not sent , error 40000")
        print("Error occured with SMTP authentication")

    logging.info("Crypto collected")
    cryptoConn.close()
    await asyncio.sleep(delay)


async def newsConnection(delay):

    conn = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
    newsConn, dbName = createDb("newsTable")  
    conn.to_sql(dbName, newsConn, if_exists='append')
    try:

        send_email(messages='Information Collected from News sources', 
                    subject=date_as, password=PASSWD)

    except EnvironmentError:
        logging.error("Mail not sent , error 40000")
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
                    subject=date_as, password=PASSWD)

    except EnvironmentError:
        logging.error("Mail not sent , error 40000")
        print("Error occured with SMTP authentication")

    logging.info("Forex collected")
    forexConn.close()
    await asyncio.sleep(delay)

async def main():

    await cryptoConnection(time_passage)
    await newsConnection(time_passage)
    await forexConnection(2)


if __name__=="__main__":

    while True:

        try:

            asyncio.run(main())

        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False
            logging.info("Progrm terminated")
            try:
                send_email(messages='Program finished', 
                        subject=date_as, password=PASSWD)
            except smtplib.SMTPAuthenticationError:
                print("Authentication error")
