import requests as req
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup as BS

from var import ConnectionVar_crypto, agent_desktop, parser, URL, ConnectionVar_forex
#from db import sqlite_conn, sqlite_table


class GetConnected():

    def __init__(self, headerToSend = agent_desktop):
        
        self.headerToSend = headerToSend

    def getHtmlFeed(self, urlToConnect):
        
        connect = req.get(urlToConnect, self.headerToSend)
        return connect.content
    
    def scrapeDataFromWeb(self, urlID=int, tag=str):

        connect = self.getHtmlFeed(URL[urlID])
        soupEverything = BS(connect, parser)
        return soupEverything


if __name__=="__main__":
    conn = GetConnected()
    print(conn.scrapeDataFromWeb(urlID=1, tag="td"))

   