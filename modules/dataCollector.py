from datetime import datetime 
import pandas as pd 
import requests
from bs4 import BeautifulSoup as soup 
from connection.var import *
from smtp import send_email
import re

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
        
        data = Connect.makeConnection(url, header)
        makeSoup = soup(data, PARSER)

        try:
            df = pd.DataFrame(index=[makeSoup.find('td', {"id":f"0_{x+1}"}).get_text().replace("\n","").replace(" ","") for x in range(0,18)],
                                columns=["LongName","CHG%","High","Bid","Low","Open"])
            df["LongName"] = [makeSoup.find('td', {"id":f"1_{x+1}"}).get_text().replace("\n","").replace("\t","") for x in range(0,18)]
            df["CHG%"] = [makeSoup.find('td', {"id":f"2_{x+1}"}).get_text() for x in range(0,18)]
            df['High'] = [makeSoup.find('td', {"id":f"4_{x+1}"}).get_text() for x in range(0,18)]
            df['Bid'] = [makeSoup.find('td', {"id":f"4_{x+1}"}).get_text() for x in range(0,18)]
            df['Low'] = [makeSoup.find('td', {"id":f"5_{x+1}"}).get_text() for x in range(0,18)]
            df['Open'] = [makeSoup.find('td', {"id":f"6_{x+1}"}).get_text() for x in range(0,18)]
            
        except ValueError:
            send_email(messages='Dafaframe valueError information not collected ftom forex', subject="Dataframe ValueError", password='<BLaNK>')
            return "Values dont match with eachother"

        return df

    
    #Connection function for cryptomarkets
    def crypto(url, header):

        #not good repeating code  somebody call police 
        data = Connect.makeConnection(url, header)
        makeSoup = soup(data, PARSER)

        #Function for checking and rearrenging coinlist
        def getCoinListNames(parsedData):
            #find all the coins
            names = [x.get_text() for x in parsedData.find_all('p', {'class':ConnectionVar_crypto['NAME']})]
            #replace all the special chars in the list
            fixedCoinList = [l.lower().replace(" ","-").replace(".","-") for l in names]
            return fixedCoinList
        #Rearrange and update coinlist
        def reArrangeCoinList(coinsToArrange):

            count = -1
            countTwo = -1
            names = getCoinListNames(makeSoup)
            words = ["polkadot","dai","omg-network","terra","elrond","golem"]
            #coins to be rearranged
            for x in names:

                count += 1

                for l in words:

                    search = re.fullmatch(l,x)
                    if search:
                        countTwo += 1
                        names[count] = coinsToBeFixed[countTwo]

            return names

        try:

            #creating a table for crypto prices    
            df = pd.DataFrame(index=[x.get_text() for x in makeSoup.find_all('p', {'class':ConnectionVar_crypto['NAME']})],
             columns=['DATE','PRICE','PRICE_CAP', 'VOLUME24','CIRCULATION'])
            df['DATE'] = datetime.strftime(datetime.now(), '%m-%d-%Y, %H:%M')
            try:
                fixedCoinList = reArrangeCoinList(coinsToBeFixed)

                assert(len(df.index) == len(fixedCoinList))#scraping prices, names etcc from coinmartketcap
                df['PRICE'] = [makeSoup.find('a',{'href':f"/currencies/{x}/markets/"}).get_text() for x in fixedCoinList] 
                #using a coin list from coinmarketcap
                df['PRICE_CAP'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['PRICE_CAP']})[1:101]]
                df['VOLUME24'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['VOLUME_24']})[:100]]
                df['CIRCULATION'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['CIRCULATION']})[:100]]
                #df['PERCENT_chg'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['PERCENT_CHG']})[:100]]
                #checking if everything is correct
                assert(len(df['PRICE']) == len(df))
                assert(len(df) == 100)

            except AssertionError:
                #if encounters assertion error then it will automaticly senda a notice
                send_email(messages='Information not Collected from coinmarketcap.com', subject="Something went BOOM", password='<BLaNK>')
                return "BOOB"

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
            send_email(messages='Dafaframe valueError information not collected ftom finviz', subject="Dataframe ValueError", password='<BLaNK>')
            return "Values dont match with eachother"

        return df

