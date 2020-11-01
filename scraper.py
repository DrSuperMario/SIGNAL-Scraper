import time

import pandas as pd

from db import createDb
from smtp import send_email
from connection.var import *
from modules.dataCollector import Connect

TIME_LOOP = True
time_passage = 120


if __name__=="__main__":

    while True:
        try:
            #Crypto Connection
            cryptoConnection = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])
            cryptoConn, dbName = createDb("CryptoTable")  
            cryptoConnection.to_sql(dbName, cryptoConn, if_exists='append')
            time.sleep(time_passage)
            #news connection
            newsConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
            newsConn, dbName = createDb("newsTable")  
            newsConnection.to_sql(dbName, newsConn, if_exists='append')
            time.sleep(time_passage)
            #Forex connection
            forexConnection = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])
            forexConn, dbName = createDb("forexTable")  
            forexConnection.to_sql(dbName, forexConn, if_exists='append')
            time.sleep(time_passage)
            #with open(f"saved/{datetime.strftime(datetime.now(), '%m-%d-%Y')}_CRYPTO.csv",'w+') as f:
            #    f.write(df.to_csv(index=True))
            #Remove password :D
            
            #send_email(messages='Information Collected', subject=date_as, password='<BLANK>')
            time.sleep(time_passage)

        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False
            cryptoConn.close()
            try:
                newsConn.close()
                cryptoConn.close()
            except NameError:
                print("Not initialized yet")
            break



