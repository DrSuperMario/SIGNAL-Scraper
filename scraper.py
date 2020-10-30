import time

import pandas as pd

from db import *
from smtp import send_email
from connection.var import *
from modules.dataCollector import Connect

TIME_LOOP = True
time_passage = 12000


if __name__=="__main__":

    while True:
        try:
            #Crypto Connection
            cryptoConnection = Connect.crypto(url=URL[1],header=HEADERS['agent_desktop'])
            cryptoConnection.to_sql(sqliteTableCrypto, sqlite_conn1, if_exists='append')
            time.sleep(time_passage)
            #news connection
            newsConnection = Connect.news(url=URL[4], header=HEADERS['agent_smartphone'])
            newsConnection.to_sql(sqliteTableNews, sqlite_conn3, if_exists='append')
            time.sleep(time_passage)
            #Forex connection
            thirdConnection = Connect.forex(url=URL[6], header=HEADERS['agent_desktop'])
            thirdConnection.to_sql(sqliteTableForex, sqlite_conn2, if_exists='append')
            time.sleep(time_passage)
            #with open(f"saved/{datetime.strftime(datetime.now(), '%m-%d-%Y')}_CRYPTO.csv",'w+') as f:
            #    f.write(df.to_csv(index=True))
            #Remove password :D
            
            #send_email(messages='Information Collected', subject=date_as, password='<BLANK>')
            time.sleep(time_passage)
        except KeyboardInterrupt:
            #print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False
            sqlite_conn.close()
            break



