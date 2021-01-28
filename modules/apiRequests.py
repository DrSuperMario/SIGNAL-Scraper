import requests as req
import logging
from datetime import datetime
from uuid import uuid4

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
except LookupError:
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

            except req.exceptions.ConnectionError or MaxRetryError:
                send_email(messages='Information Not sent to API: Cryptolist', 
                        subject=f"{str(datetime.now())} API Connection Crypto", password=PASSWD)
                logging.error("error sending news data to API Cryptolist")
                return "Connection not made", 404

            except NewConnectionError:
                send_email(messages='Information Not sent to API New Conenction error: Cryptolist', 
                        subject=f"{str(datetime.now())} API Connection Error Crypto", password=PASSWD)
                logging.error("error sending news data to API Cryptolist")
                return "Connection not made", 404
            
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
                
                return "Data Sent",201

            except req.exceptions.ConnectionError or MaxRetryError:
                send_email(messages='Information Not sent to API: Newslist', 
                        subject=f"{str(datetime.now())} API Connection News", password=PASSWD)
                logging.error("error sending news data to API Newslist")
                return "Connection not made", 404

            except NewConnectionError:
                send_email(messages='Information Not sent to API New Conenction error: Newslist', 
                        subject=f"{str(datetime.now())} API Connection Error News", password=PASSWD)
                logging.error("error sending news data to API Newslist")
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
                
                return "data sent",201

            except req.exceptions.ConnectionError or MaxRetryError:
                send_email(messages='Information Not sent to API: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Forex", password=PASSWD)
                logging.error("error sending news data to API Forexlist")
                return "Connection not made", 404

            except NewConnectionError:
                send_email(messages='Information Not sent to API New Conenction error: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Error Forex", password=PASSWD)
                logging.error("error sending news data to API Forexlist")
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
                
                return "data sent",201

            except req.exceptions.ConnectionError or MaxRetryError:
                send_email(messages='Information Not sent to API: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Forex", password=PASSWD)
                logging.error("error sending news data to API Forexlist")
                return "Connection not made", 404

            except NewConnectionError:
                send_email(messages='Information Not sent to API New Conenction error: Forexlist', 
                        subject=f"{str(datetime.now())} API Connection Error Forex", password=PASSWD)
                logging.error("error sending news data to API Forexlist")
                return "Connection not made", 404
        


        else:
            return "Type not set . select type (news, forex, crypto)"

    def getPost(self):
        data = req.get(f"http://{self.apiloc}/newslist")
        return data.json



    
    