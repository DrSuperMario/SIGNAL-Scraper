import requests as req
from datetime import datetime

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

from connection.var import *


SIA = SentimentIntensityAnalyzer()

class RequestAPI():

    def __init__(self, url=None, apiloc=Constants.API_ADDRESS.value, data=None):
        
        self.url = url
        self.apiloc = apiloc
        self.data = data

    def analyseData(self):
        polarity = []
        for x in range(len(self.data)):
            polarity.append(SIA.polarity_scores(self.data['headLine'][x]))
        df = pd.DataFrame(polarity, columns=['neg','neu','pos'])
        return df


    @classmethod    
    def sendPost(cls, dataToSend):
        for x in range(len(cls.dataToSend)):
            data = req.post(cls.apiloc + str(x) , data = {
                            "newsArticle":dataToSend['newsHeadline'][x],
                            "newsPolarityNeg":dataToSend['neg'][x],
                            "newsPolarityPos":dataToSend['pos'][x],
                            "newsPolarityNeu":dataToSend['neu'][x]
        })
        return "Data Sent",200

    @classmethod
    def getPost(cls):
        data = req.get(cls.apiloc)
        return data.json



    
    