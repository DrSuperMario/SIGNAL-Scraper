import requests as req
import logging
from datetime import datetime
from uuid import uuid4

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except LookupError as le:
    logging.error("ERROR vader_lexicon not found " + le.__name__)
    import nltk
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer


import pandas as pd
from urllib3.exceptions import MaxRetryError, NewConnectionError

from smtp import send_email
from connection.var import *

#Initializing NLTk.Vaher sentimentanalyzer
SIA = SentimentIntensityAnalyzer()

class RequestAPI():

    """
    Class for sending scraped data to Serverside API

    sendPost() - Send scraped data to api
    getPost() - get scraped data from API

    Params:

        url - default None , no implementation . Removing soon
        apiloc - IP or URL of API
        data - datasource to send to API


    """

    def __init__(self, url=None, apiloc=Constants.API_ADDRESS.value):
        #initalize params
        self.url = url
        self.apiloc = apiloc

    def sendPost(self ,data, source_type=None):

        if source_type=="crypto".lower():
            
            data['NAME'] = data.index.to_list()
            data.reset_index(drop=True, inplace=True)
            dataToSend = data
            try:
                _id = "1x5678Tr24Xpn677Ss"
                delete = req.delete(f"http://{self.apiloc}/crypto/{_id}")

                for x in range(len(dataToSend)):
                        
                    data = req.post(f"http://{self.apiloc}/crypto/" + str(uuid4()), json = {
                                    "cryptoName":dataToSend['NAME'][x],
                                    "cryptoDate":dataToSend['DATE'][x],
                                    "cryptoPrice":dataToSend['PRICE'][x],
                                    "cryptoPriceCap":dataToSend['PRICE_CAP'][x],
                                    "cryptoVolume":dataToSend['VOLUME24'][x],
                                    "cryptoCirculation":dataToSend['CIRCULATION'][x]
                })

            except req.exceptions.ConnectionError or MaxRetryError as ce:
                send_email(messages='Information Not sent to API: Cryptolist', 
                        subject=f"{str(datetime.now())} API Connection Crypto", password=PASSWD)
                logging.error("ERROR sending cryptoData to API Cryptolist " + ce.__doc__)
                return "Connection not made", 404

            except NewConnectionError as nce:
                send_email(messages='Information Not sent to API New Conenction error: Cryptolist', 
                        subject=f"{str(datetime.now())} API Connection Error Crypto", password=PASSWD)
                logging.error("ERROR sending cryptoData to API Cryptolist " + nce.__doc__)
                return "Connection not made", 404
            
            
            logging.info("INFO Data sent to CryptoAPI")
            return "data sent",201

        elif source_type=="news".lower():

            polarity = []
            for x in range(len(data)):
                polarity.append(SIA.polarity_scores(data['headLine'][x]))
            #comparing lenghts 
            assert(len(polarity) == len(data))

            dataToSend = pd.DataFrame(polarity, columns=['neg','neu','pos','date'])
            dataToSend['date'] = data.index.to_list()
            dataToSend.reset_index(drop=True, inplace=True)
            data.reset_index(drop=True, inplace=True)
            dataToSend = pd.concat([data, dataToSend], axis=1)


            try:
                #error hanfling if connection isnt made with a server
                _id = "1x5678Tr24Xpn677Ss"
                delete = req.delete(f"http://{self.apiloc}/news/{_id}")
            
            
                for x in range(len(dataToSend)):
                    
                    data = req.post(f"http://{self.apiloc}/news/" + str(uuid4()), data = {
                                    "newsArticle":dataToSend['headLine'][x],
                                    "newsArticleWWW":dataToSend['www'][x],
                                    "newsPolarityNeg":dataToSend['neg'][x],
                                    "newsPolarityPos":dataToSend['pos'][x],
                                    "newsPolarityNeu":dataToSend['neu'][x],
                                    "creationDate":dataToSend['date'][x]
                })

                logging.info("INFO Data sent to NewsAPI")
                return "Data Sent",201

            except req.exceptions.ConnectionError or MaxRetryError as rec:
                send_email(messages='Information Not sent to API: Newslist', 
                        subject=f"{str(datetime.now())} API Connection News", password=PASSWD)
                logging.error("ERROR sending newsData to API Newslist " + rec.__doc__)
                return "Connection not made", 404

            except NewConnectionError as mce:
                send_email(messages='Information Not sent to API New Conenction error: Newslist', 
                        subject=f"{str(datetime.now())} API Connection Error News", password=PASSWD)
                logging.error("ERROR sending newsData to API Newslist " + mce.__doc__)
                return "Connection not made", 404
           

        elif source_type=="forex".lower():
            
            #data['NAME'] = data.index.to_list()
            #data.reset_index(drop=True, inplace=True)
            dataToSend = data
            
            try:
                _id = "1x5678Tr24Xpn677Ss"
                delete = req.delete(f"http://{self.apiloc}/forex/{_id}")

                for x in range(len(dataToSend)):
                        
                    data = req.post(f"http://{self.apiloc}/forex/" + dataToSend.index[x], json = {
                                    "forexName":dataToSend['LongName'][x],
                                    "forexChange":dataToSend['CHG%'][x],
                                    "forexHigh":dataToSend['High'][x],
                                    "forexBid":dataToSend['Bid'][x],
                                    "forexLow":dataToSend['Low'][x],
                                    "forexOpen":dataToSend['Open'][x]
                })

                logging.info("INFO Data sent to ForexAPI")
                return "data sent",201

            except req.exceptions.ConnectionError or MaxRetryError as rec:
                send_email(messages='Information Not sent to API: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Forex", password=PASSWD)
                logging.error("ERROR sending forexData to API Forexlist " + rec.__doc__)
                return "Connection not made", 404

            except NewConnectionError as nce:
                send_email(messages='Information Not sent to API New Conenction error: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Error Forex", password=PASSWD)
                logging.error("ERROR sending forexData to API Forexlist " + nce.__doc__)
                return "Connection not made", 404
        
        elif source_type=='stock'.lower():
            dataToSend = data

            try:
                _id = "1x5678Tr24Xpn677Ss"
                delete = req.delete(f"http://{self.apiloc}/stock/{_id}")

                for x in range(len(dataToSend)):
                        
                    data = req.post(f"http://{self.apiloc}/stock/" + dataToSend.index[x], json = {
                                    "stockName":dataToSend.index[x],
                                    "stockLow":dataToSend['Low'][x],
                                    "stockLast":dataToSend['Last'][x],
                                    "stockHigh":dataToSend['High'][x],
                                    "stockChg":dataToSend['Chg'][x],
                                    "stockChgp":dataToSend['Chg%'][x]
                })
                
                logging.info("INFO Data sent to StockAPI")
                return "data sent",201

            except req.exceptions.ConnectionError or MaxRetryError as rec:
                send_email(messages='Information Not sent to API: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Forex", password=PASSWD)
                logging.error("ERROR sending forexData to API Forexlist " + rec.__doc__)
                return "Connection not made", 404

            except NewConnectionError as nce:
                send_email(messages='Information Not sent to API New Conenction error: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Error Forex", password=PASSWD)
                logging.error("ERROR sending forexData to API Forexlist " + nce.__doc__)
                return "Connection not made", 404
        


        else:
            return "Type not set . select type (news, forex, crypto)"

    def getPost(self):
        data = req.get(f"http://{self.apiloc}/newslist")
        return data.json



    
    