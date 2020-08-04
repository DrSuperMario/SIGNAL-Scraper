import requests as req 
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup as BS

from connection.var import ConnectionVar, agent_desktop, parser, URL


header = {'User-Agent': agent_desktop}

def get_html(url, header):
    #get data from sources
    #url for various sources
    connect = req.get(url, header)
    data = connect.content
    return data

if __name__=="__main__":
    conn = get_html(URL[1], header=agent_desktop)
    soup = BS(conn, parser)

    all_name = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['NAME'])]
    all_price = [x.get_text() for x in soup.find_all('td',class_=ConnectionVar['PRICE'])]
    all_pricecap = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['PRICE'])]
    all_volume24 = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['VOLUME_24'])]
    all_circulation = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['CIRCULATION'])]
    all_percent = [x.get_text() for x in soup.find_all('td', class_=ConnectionVar['PERCENT_CHG'])]

    df = pd.DataFrame(index=all_name, columns=['PRICE','PRICE_CAP', 'VOLUME24','CIRCULATION', 'PERCENT_chg'])

    df['PRICE'] = all_price
    df['PRICE_CAP'] = all_pricecap
    df['VOLUME24'] = all_volume24
    df['CIRCULATION'] = all_circulation
    df['PERCENT_chg'] = all_percent


    with open(f"saved/{datetime.strftime(datetime.now(), '%m-%d-%Y')}_CRYPTO.csv",'w+') as f:
        f.write(df.to_csv(index=True))




