import asyncio
from datetime import datetime


from modules.dataCollector import Connect
from connection.var import *
from db import createDb
from smtp import send_email


TIME_LOOP = True
time_passage = 12000
date_as = str(datetime.now())
passwd = '<BLANK>'


async def cryptoConnection(delay):

    conn = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])

    cryptoConn, dbName = createDb("CryptoTable")  
    conn.to_sql(dbName, cryptoConn, if_exists='append')
    try:

        send_email(messages='Information Collected from Crypto Source',
                     subject=date_as, password=passwd)
    
    except EnvironmentError:
        print("Error occured with SMTP authentication")

    await asyncio.sleep(delay)


async def newsConnection(delay):

    conn = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
    newsConn, dbName = createDb("newsTable")  
    conn.to_sql(dbName, newsConn, if_exists='append')
    try:

        send_email(messages='Information Collected from News sources', 
                    subject=date_as, password=passwd)

    except EnvironmentError:
        print("Error occured with SMTP authentication")

        await asyncio.sleep(delay)

async def forexConnection(delay):

    #Forex connection
    conn = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])
    forexConn, dbName = createDb("forexTable")  
    conn.to_sql(dbName, forexConn, if_exists='append')
    try:

        send_email(messages='Information Collected from News sources', 
                    subject=date_as, password=passwd)

    except EnvironmentError:
        print("Error occured with SMTP authentication")

        await asyncio.sleep(delay)

async def main():

    await cryptoConnection(time_passage)
    await newsConnection(time_passage)
    await forexConnection(3600)


if __name__=="__main__":

    while True:

        try:

            asyncio.run(main())

        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False
            conn.close()
