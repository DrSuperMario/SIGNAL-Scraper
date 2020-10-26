from datetime import datetime 
import pandas as pd 
import requests
from bs4 import BeautifulSoup as soup 
from connection.var import *
from smtp import send_email

#
# make use of a class structure
#


class Connect():

    #start connection initialization
    def makeConnection(url, header):
        #check if connection can be made and no errors are raised
        try:
            conn = requests.get(url,headers={'User-Agent':header})
        except requests.exceptions.ConnectionError:
            return "Invalid URL", 404
        #checking id the status code is 200
        if conn.status_code == requests.codes.ok:
            return conn.content
        else:
            try:
                #if the connection fails then turn to the default 
                conn = requests.get(URL[4], headers={'User-Agent':HEADERS['agent_desktop']})
                return conn.content
            #just if someting goes horribly wrong
            except requests.exceptions.HTTPError:
                #send an email to let me know if there was OOPS
                send_email(messages='Information not Collected', subject="Something went BOOM", password='<BLaNK>')
                return "Something made OOPS", 404

    #connection function for forex
    def forex(url, header):
        pass 
    
    #Connection function for cryptomarkets
    def crypto(url, header):

        #not good repeating code  somebody call police 
        data = Connect.makeConnection(url, header)
        makeSoup = soup(data, PARSER)

        try:
            df = pd.DataFrame(index=[x.get_text() for x in makeSoup.find_all('p', {'class':ConnectionVar_crypto['NAME']})],
             columns=['DATE','PRICE','PRICE_CAP', 'VOLUME24','CIRCULATION', 'PERCENT_chg'])
            df['DATE'] = datetime.strftime(datetime.now(), '%m-%d-%Y, %H:%M')
            df['PRICE'] = [x.get_text() for x in makeSoup.find_all('td',{'class':'rc-table-cell font_weight_500___2Lmmi'})[:100]]
            df['PRICE_CAP'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['PRICE_CAP']})[:100]]
            df['VOLUME24'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['VOLUME_24']})[:100]]
            df['CIRCULATION'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['CIRCULATION']})[:100]]
            df['PERCENT_chg'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['PERCENT_CHG']})[:100]]
            return df
        except ValueError:
            return 0

    
    #Connectionfunction for news markets
    def news(url, header):

        data = Connect.makeConnection(url, header)
        makeSoup = soup(data, PARSER)
        
        try:
            df = pd.DataFrame(index=[x.get_text() for x in makeSoup.find_all('td',{'class':'nn-date'})[1:90]],
                            columns=['headLine','www'])
            df['headLine'] = [x.get_text() for x in makeSoup.find_all('a',{'class':'nn-tab-link'})[1:90]]
            df['www'] = [x.get('href') for x in makeSoup.find_all('a', {'class':'nn-tab-link'})[1:90]]
        #Check if data is excact and if not then send an email
        except ValueError:
            send_email(messages='Dafaframe valueError', subject="Dataframe ValueError", password='<BLaNK>')
            return "Values dont match with eachother"

        return df

