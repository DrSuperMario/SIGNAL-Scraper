import requests as req
import logging
from datetime import datetime

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

from smtp import send_email
from connection.var import *


SIA = SentimentIntensityAnalyzer()

class RequestAPI():

    def __init__(self, url=None, apiloc=Constants.API_ADDRESS.value):
        
        self.url = url
        self.apiloc = apiloc

    def sendPost(self ,data):

        polarity = []
        for x in range(len(data)):
            polarity.append(SIA.polarity_scores(data['headLine'][x]))
        
        assert(len(polarity) == len(data))

        dataToSend = pd.DataFrame(polarity, columns=['neg','neu','pos'])
        dataToSend.reset_index(drop=True, inplace=True)
        data.reset_index(drop=True, inplace=True)
        dataToSend = pd.concat([data, dataToSend], axis=1)

        try:
        
            for x in range(len(dataToSend)):
                data = req.post(f"http://{self.apiloc}/postnews/" + dataToSend['headLine'][x][:-1].replace(" ","-").replace(",","").replace("\"","-").replace("\'","").lower() , data = {
                                "newsArticle":dataToSend['headLine'][x],
                                "newsArticleWWW":dataToSend['www'][x],
                                "newsPolarityNeg":dataToSend['neg'][x],
                                "newsPolarityPos":dataToSend['pos'][x],
                                "newsPolarityNeu":dataToSend['neu'][x]
            })

            return "Data Sent",201

        except req.exceptions.ConnectionError:
            send_email(messages='Information Not sent to API', 
                    subject=str(datetime.now()), password=PASSWD)
            logging.error(f"{datetime.now()} error sending news data to API")
            return "Connection not made", 404
   
    def getPost(self):
        data = req.get(f"http://{self.apiloc}/newslist")
        return data.json



    
    