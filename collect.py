import requests as req
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup as BS

from connection.var import ConnectionVar_crypto, agent_desktop, parser, URL, ConnectionVar_forex
from db import sqlite_conn, sqlite_table

df_columns = ['DATE','PRICE','PRICE_CAP', 'VOLUME_24','CIRCULATION', 'PERCENT_CHG']
data_columns = ['NAME','PRICE','PRICE_CAP', 'VOLUME_24','CIRCULATION', 'PERCENT_CHG']
tag_names = ['a','td']
 

def get_html(url, header):
    #get data from sources
    #url for various sources
    connect = req.get(url, header)
    data = connect.content
    return data

def scrape_data_from_web(where, tag, id_name, url_id):

    conn = get_html(URL[url_id], header=agent_desktop)
    soup = BS(conn, parser)

    date_as = datetime.strftime(datetime.now(), '%m-%d-%Y, %H:%M')
    scraped_data = []

    for t, n in tag, id_name:
        scraped_data.append([x.get_text() for x in soup.find_all(t, class_=ConnectionVar_crypto[n])])
    
    if where == 'crypto':
        df = pd.DataFrame(index=scraped_data[0], columns=df_columns)

        df['DATE'] = date_as
        df['PRICE'] = scraped_data[1]
        df['PRICE_CAP'] = scraped_data[2]
        df['VOLUME_24'] = scraped_data[3]
        df['CIRCULATION'] = scraped_data[4]
        df['PERCENT_CHG'] = scraped_data[5]

        df.to_sql(sqlite_table, sqlite_conn, if_exists='append')

    elif where == 'forex':
        df = pd.DataFrame(index=scraped_data[0], columns=df_columns)

        df['DATE'] = date_as
        df['PRICE'] = scraped_data[1]
        df['PRICE_CAP'] = scraped_data[2]
        df['VOLUME_24'] = scraped_data[3]
        df['CIRCULATION'] = scraped_data[4]
        df['PERCENT_CHG'] = scraped_data[5]

        #df.to_sql(sqlite_table, sqlite_conn, if_exists='append')
        return df.head(19)


if __name__=="__main__":
    print(scrape_data_from_web(where='forex', tag=tag_names, url_id=0, id_name=data_columns))