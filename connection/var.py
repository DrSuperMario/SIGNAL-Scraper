from enum import Enum

"""
Library where alla the variables are held

Constants(enum) - using python enumerate to not randomly owerwite vars. 

Params:
    LOOP_TIME  - time how long the sleep should be between each iteration
    LOOP_END_TIME - time between the las loop
    API_ADDRESS - URL or IP for sending data to API
    FALLBACK_ADDR - URL or IP to run a dead mans switch on if something should fail
    FALLBACK_PORT - port to use with the dead man switch

    ALLOW_FALLBACK - Boolean to activate DMS
    SEND_NOTIFICATION - Boolean True if you would like to get an email notification
    SEND_TO_API - Boolean True if Data is to be send to API
    URL - URLs for diffrent sources to scrape data
    PARSER - parser to be used with beautifulsoup
    PASSWD - Password to be used with the send_mail()
    HEADERS - diffrent header to choose from to make a requests

    ConnectionVar_crypto---->
    ConnectionVar_forex ------->  dicts for tags to be search from scraped pages
    connectionVar_news----->

    fixedCoinListVar - list of crypto coins that needed to be replaced
    coinsToBeFixed - new list items that will replace the old for the scraper
    
"""

class Constants(Enum):

    LOOP_TIME = 1
    LOOP_END_TIME = 2
    API_ADDRESS = "brinenewsapi.herokuapp.com"
    FALLBACK_ADDR = "165.227.149.157"
    FALLBACK_PORT = 5001
    TIME_TO_COLLECT = '18'

#GLOBAL SETTINGS
SEND_NOTIFICATION = False
SEND_TO_API = True
ALLOW_FALLBACK = False

#Smtp settings
PASSWD = "<blank>" # server password
EMAIL_PORT = 465 #server port
SMTP_SERVER = 'smtp.gmail.com' #server aadress
SENDER_EMAIL = 'muukmario@gmail.com' #email
RECIVER_EMAIL = 'mario@pythonslack.com' #reciver email

URL = ("https://www.tradingview.com/markets/currencies/rates-all/",
       "https://coinmarketcap.com/",
       "https://www.hl.co.uk/shares/stock-market-news",
       "https://www.ft.com/news-feed",
       "https://finviz.com/news.ashx",
       "https://www.coingecko.com/en/coins/all",
       "https://uk.advfn.com/forex/live-prices",
       "https://goldprice.org/cryptocurrency-price",
       "https://www.kitco.com/market/",
       "https://www.investing.com/indices/major-indices")

PARSER = "html.parser"



HEADERS = {
    'agent_desktop':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
        'Safari/537.36',
        'agent_smartphone':
        'Mozilla/5.0 (Linux; Android 9; SM-G960F '
        'Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36',
        'agent_old_smartphone':
        'Mozilla/5.0 (Linux; Android 9; SM-G960F '
        'Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'
}

ConnectionVar_crypto = {
    "NAME": "Text-sc-1eb5slv-0 iTmTiC",
    "PRICE": "no-wrap",
    "PRICE_CAP": "Text-sc-1eb5slv-0 hVAibX",
                 "VOLUME_24": "Box-sc-16r8icm-0 sc-1anvaoh-0 gxonsA",
                 "CIRCULATION": "Text-sc-1eb5slv-0 kqPMfR",
                 "PERCENT_CHG": "Text-sc-1eb5slv-0 PercentageChange__ChangeText-sc-1siv958-1 jRHnTF"
}

ConnectionVar_forex = {
    "a": "tv-screener__symbol",
    "td": "tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big"

}

connectionVar_news = {
    "a": "nn-tab-link",
    "td": "nn-date"
}

fixedCoinListVar = ["polkadot","dai","omg-network","terra","elrond","golem","synthetix"]
coinsToBeFixed = ["polkadot-new","multi-collateral-dai","omg","terra-luna",
                   "elrond-egld","golem-network-tokens","synthetix-network-token"]
