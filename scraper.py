import requests as req 
from datetime import datetime
import time

import pandas as pd
from bs4 import BeautifulSoup as BS
from db import sqlite_conn, sqlite_table

from connection.var import ConnectionVar, agent_desktop, parser, URL
from smtp import send_email


header = {'User-Agent': agent_desktop}
TIME_LOOP = True
time_passage = 36

def get_html(url, header):
    #get data from sources
    #url for various sources
    connect = req.get(url, header)
    data = connect.content
    return data

if __name__=="__main__":
    while True:
        try:
            conn = get_html(URL[1], header=agent_desktop)
            soup = BS(conn, parser)

            date_as = datetime.strftime(datetime.now(), '%m-%d-%Y, %H:%M')

            all_name = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['NAME'])]
            all_price = [x.get_text() for x in soup.find_all('td',class_=ConnectionVar['PRICE'])]
            all_pricecap = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['PRICE_CAP'])]
            all_volume24 = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['VOLUME_24'])]
            all_circulation = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['CIRCULATION'])]
            all_percent = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['PERCENT_CHG'])]

            df = pd.DataFrame(index=all_name, columns=['DATE','PRICE','PRICE_CAP', 'VOLUME24','CIRCULATION', 'PERCENT_chg'])

            df['DATE'] = date_as
            df['PRICE'] = all_price
            df['PRICE_CAP'] = all_pricecap
            df['VOLUME24'] = all_volume24
            df['CIRCULATION'] = all_circulation
            df['PERCENT_chg'] = all_percent


            df.to_sql(sqlite_table, sqlite_conn, if_exists='append')

            #with open(f"saved/{datetime.strftime(datetime.now(), '%m-%d-%Y')}_CRYPTO.csv",'w+') as f:
            #    f.write(df.to_csv(index=True))
            send_email(messages='Information Collected', subject=date_as, password='Haxx0r001')
            time.sleep(time_passage)
        except KeyboardInterrupt:
            print(f'Run canceled on {datetime.now()}')
            TIME_LOOP = False
            sqlite_conn.close()
            break



