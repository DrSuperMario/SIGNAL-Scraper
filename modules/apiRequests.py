import requests as req
import logging
from datetime import datetime
from uuid import uuid4

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

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

    def sendPost(self ,data, type=None):

        if type=="crypto".lower():
            
            data['NAME'] = data.index.to_list()
            data.reset_index(drop=True, inplace=True)
            dataToSend = data

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
            
            return "data sent",201

        elif type=="news".lower():

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
                req.delete(f"http://{self.apiloc}/news/{_id}")
            
            
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

            except req.exceptions.ConnectionError:
                send_email(messages='Information Not sent to API', 
                        subject=str(datetime.now()), password=PASSWD)
                logging.error(f"{datetime.now()} error sending news data to API")
                return "Connection not made", 404

        elif type=="forex":
            
            #data['NAME'] = data.index.to_list()
            #data.reset_index(drop=True, inplace=True)
            dataToSend = data

            _id = "1x5678Tr24Xpn677Ss"
            req.delete(f"http://{self.apiloc}/forex/{_id}")

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

        else:
            return "Type not set . select type (news, forex, crypto)"

    def getPost(self):
        data = req.get(f"http://{self.apiloc}/newslist")
        return data.json



    
    