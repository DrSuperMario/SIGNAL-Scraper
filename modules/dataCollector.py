from datetime import datetime
import requests
import re
import logging
from textwrap import dedent

#Log file location

import pandas as pd 
from bs4 import BeautifulSoup as soup
from urllib3.exceptions import ReadTimeoutError 


from connection.var import *
from smtp import send_email
from modules.apiRequests import RequestAPI


#
# make use of a class structure
#

#start logging
#logging.basicConfig(filename=os.path.normpath('log/dataCollector.log'))

class Connect():

    """
    module for connecting diffrent connection elements together

    forex() - for scraping forex data
    crypto()  - for scraping crypto data
    news()  -  for scraping news data
    
    params: 

        url - passing right URL from connection.var
        header - header to send with a requests
    
    for sources:

        reqToSend - boolean for sending data to API
        send_notification - boolean for sending notifications to email

    Will implement preciOus metal quote scraper in a later release

    """

    #start connection initialization
    def makeConnection(url, header):
        #check if connection can be made and no errors are raised
        try:
            conn = requests.get(url,headers={'User-Agent':header}, timeout=(3.05, 90))
        except requests.exceptions.ConnectionError:
            logging.error("Invalid URL")
            return "Invalid URL", 404
        except requests.exceptions.ReadTimeout or ReadTimeoutError:
            logging.info("ReadTimeoutError")
            conn = requests.get(url,headers={'User-Agent':header}, timeout=None)

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
                logging.error("HTTP Connection not made")
                send_email(messages=f"Information not Collected time: {str(datetime.now())}", 
                            subject="Something went BOOM", password=PASSWD)
                return "Something made OOPS", 404
            except requests.exceptions.ReadTimeout or ReadTimeoutError:
                logging.error("HTTP Connection not made ReadTimeOut")
                send_email(messages=f"Information not Collected time: {str(datetime.now())}", 
                            subject="Something went BOOM. ReadTimeOut", password=PASSWD)
                return "Something made OOPS", 404
            

    #connection function for forex
    def forex(url, header, reqToSend=False, send_notification=False):
        
        data = Connect.makeConnection(url, header)
        
        try:
            makeSoup = soup(data, PARSER)

        except TypeError:
            logging.error("Info not collected from Forexsource")
            send_email(messages=f"Information not Collected from ForexList time: {str(datetime.now())}",
                        subject="Something went BOOM with forex", password=PASSWD)
            return None
        

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
            logging.error("Forex: ValueERROR")
            return None
        
        except AttributeError:
            logging.error("Forex: NoneType has no attribute get_text")
         

            if(send_notification):
                send_email(messages=f"Dafaframe valueError information not collected ftom forex time: {str(datetime.now())}", 
                            subject="Dataframe ValueError", password=PASSWD)

            return None
        if(reqToSend):
            RequestAPI().sendPost(data=df, source_type="forex")

        logging.info("Forex collected")
        return df

    
    #Connection function for cryptomarkets
    def crypto(url, header, reqToSend=False, send_notification=False):

            #if the first site fails automaticly scrape from anathor
        def backupCoinList():
            try:    
                data = Connect.makeConnection(url=URL[7], header=HEADERS['agent_desktop'])

                if(data != None):
                    try:
                        makeSoup = soup(data, PARSER)

                    except TypeError:
                        logging.error("Backup info not collected from coinlist")
                        send_email(messages=f"Information not Collected from backupCoinList time: {str(datetime.now())}",
                                    subject="Something went BOOM with backup", password=PASSWD)
                        return None
                else:
                    logging.error("Falling back from backupCoinlist")
                    return None
                
                df = pd.DataFrame(index=[x.get_text().replace("\n","").replace("\xa0","") for x in makeSoup.find_all('td',{'class':'views-field views-field-field-crypto-proper-name'})],
                                    columns=['DATE','PRICE','PRICE_CAP', 'VOLUME24','CIRCULATION'])
                #build dataframe for the backup source
                df['DATE'] = datetime.strftime(datetime.now(), '%m-%d-%Y, %H:%M')
                df['PRICE'] = [dedent(x.get_text().replace("\n","").replace("        ","")) for x in makeSoup.find_all('td',{'class':'views-field views-field-field-crypto-price views-align-right'})]
                df['PRICE_CAP'] = [dedent(x.get_text().replace("\n","").replace("        ","")) for x in makeSoup.find_all('td',{'class':'views-field views-field-field-market-cap views-align-right hidden-xs'})]
                df['VOLUME24'] =  [dedent(x.get_text().replace("\n","").replace("        ","")) for x in makeSoup.find_all('td',{'class':'views-field views-field-field-crypto-volume views-align-right hidden-xs'})]
                df['CIRCULATION'] = [dedent(x.get_text().replace("\n","").replace("        ","")) for x in makeSoup.find_all('td',{'class':'views-field views-field-field-crypto-circulating-supply views-align-right'})]
                
                if(send_notification):
                    send_email(messages=f"Information Collected from backupCoinList time: {str(datetime.now())}",
                                subject="Information collectd", password=PASSWD)
                
                if(reqToSend):
                    RequestAPI().sendPost(data=df, source_type="crypto")


                logging.info("Crypto collected")

                return df

            except ValueError:
                logging.error("Backup info not collected from coinlist")
                return None

        #not good repeating code  somebody call police 
        data = Connect.makeConnection(url, header)
        try:
            makeSoup = soup(data, PARSER)
        except TypeError:
            return backupCoinList()  

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
            #coins to be rearranged
            for x in names:
                count += 1
                for l in fixedCoinListVar:
                    search = re.fullmatch(l,x)
                    if search:
                        countTwo += 1
                        names[count] = coinsToArrange[countTwo]
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
                df['VOLUME24'] = [x.get_text() for x in makeSoup.find_all('div',{'class':ConnectionVar_crypto['VOLUME_24']})[:100]]
                df['CIRCULATION'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['CIRCULATION']})[:100]]
                #df['PERCENT_chg'] = [x.get_text() for x in makeSoup.find_all('p',{'class':ConnectionVar_crypto['PERCENT_CHG']})[:100]]
                #checking if everything is correct
                assert(len(df['PRICE']) == len(df))
                assert(len(df) == 100)

            except AssertionError:
                #if encounters assertion error then it will automaticly senda a notice
                logging.error("Assertion error from coinlist")

                if(send_notification):
                    send_email(messages=f"Information not Collected from coinmarketcap.com time: {str(datetime.now())}",
                                subject="Something went BOOM", password=PASSWD)

                return backupCoinList()

            return df

        except ValueError or None:
            logging.error("Valueerror from cryptocoinlist")
            return backupCoinList()

    
    #Connectionfunction for news markets
    def news(url, header, reqToSend=False, send_notification=False):

        data = Connect.makeConnection(url, header)

        if(data != None):

            try:
                makeSoup = soup(data, PARSER)

            except TypeError:
                logging.error("Info not collected from Newslist")
                send_email(messages=f"Information not Collected from NewsList time: {str(datetime.now())}",
                            subject="Something went BOOM with news", password=PASSWD)
                return None
        else:
            logging.info("Falling back")
            return None
                

        try:
            df = pd.DataFrame(index=[x.get_text() for x in makeSoup.find_all('td',{'class':'nn-date'})[1:90]],
                            columns=['headLine','www'])
            df['headLine'] = [x.get_text() for x in makeSoup.find_all('a',{'class':'nn-tab-link'})[1:90]]
            df['www'] = [x.get('href') for x in makeSoup.find_all('a', {'class':'nn-tab-link'})[1:90]]
        #Check if data is excact and if not then send an email
        except ValueError:
            logging.error("Value error from newsSource")

            if(send_notification):
                send_email(messages=f"Dafaframe valueError information not collected ftom finviz time: {str(datetime.now())}", 
                            subject="Dataframe ValueError", password=PASSWD)

            return None
        #check if user would like to send data to API
        if(reqToSend):
            RequestAPI().sendPost(data=df, source_type='news')

        logging.info("News collected")
        
        return df


    def stock(url, header, reqToSend=False, send_notification=False):

        data = Connect.makeConnection(url, header)

        if(data != None):

            try:
                makeSoup = soup(data, PARSER)

            except TypeError:
                logging.error("Info not collected from Stocklist")
                send_email(messages=f"Information not Collected from StockList time: {str(datetime.now())}",
                            subject="Something went BOOM with stock", password=PASSWD)
                makeSoup = None
        else:
            logging.error("Falling back stockdata not collected ")
            return None
                
        
        def find_elements(to_search =''):
            yield re.findall(r'pid-\d+-'+to_search,str(makeSoup))
            
        def find_pc():
            yield re.findall(r'bold greenFont pid-\d+-\bpc\b|bold redFont pid-\d+-\bpc\b|bold blackFont pid-\d+-\bpc\b',
                                str(makeSoup.find_all('td')),re.M)
        def find_pcp():
            yield re.findall(r'bold greenFont pid-\d+-\bpcp\b|bold redFont pid-\d+-\bpcp\b|bold blackFont pid-\d+-\bpcp\b',
                                str(makeSoup.find_all('td')),re.M)
        
        try:
            df = pd.DataFrame(index=[i.get_text() for i in makeSoup.find_all('td',{'class':'bold left plusIconTd noWrap elp'})],
                                            columns=["Low","Last","High","Chg","Chg%"])
            df['Low'] = [j.get_text() for j in [makeSoup.find_all('td',{'class':i}) for i in find_elements(to_search='low')][0][:45]]
            df['Last'] = [j.get_text() for j in [makeSoup.find_all('td',{'class':i}) for i in find_elements(to_search='last')][0][:45]]
            df['High'] = [j.get_text() for j in [makeSoup.find_all('td',{'class':i}) for i in find_elements(to_search='high')][0][:45]]
            df['Chg'] = [j.get_text() for j in [makeSoup.find_all('td',{'class':i}) for i in find_pc()][0]]
            df['Chg%'] = [j.get_text() for j in [makeSoup.find_all('td',{'class':i}) for i in find_pcp()][0]]
        
        except ValueError:
            logging.error("Value error from StockSource")

            if(send_notification):
                send_email(messages=f"Dafaframe valueError information not collected ftom stocklist time: {str(datetime.now())}", 
                            subject="Dataframe ValueError", password=PASSWD)

            return None
        #check if user would like to send data to API
        if(reqToSend):
            RequestAPI().sendPost(data=df, source_type='stock')

        logging.info("Stock collected")

        return df
    #Collect metal prices
    #Not jet implemented SOON
    def preciousMetals(url, header):

        data = Connect.makeConnection(url, header)
        makseSoup = soup(data, PARSER)

    try:
        pass
    except ValueError:
        pass

