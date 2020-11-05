from enum import Enum



class Constants(Enum):

    LOOP_TIME = 12000
    LOOP_END_TIME = 6400
    API_ADDRESS = "127.0.0.1:5050"



URL = ("https://www.tradingview.com/markets/currencies/rates-all/",
       "https://coinmarketcap.com/",
       "https://www.hl.co.uk/shares/stock-market-news",
       "https://www.ft.com/news-feed",
       "https://finviz.com/news.ashx",
       "https://www.coingecko.com/en/coins/all",
       "https://uk.advfn.com/forex/live-prices",
       "https://goldprice.org/cryptocurrency-price",
       "https://www.kitco.com/market/")

PARSER = "html.parser"

PASSWD = "<blank>"

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

fixedCoinList = ["polkadot","dai","omg-network","terra","elrond","golem"]
coinsToBeFixed = ["polkadot-new","multi-collateral-dai","omg","terra-luna",
                   "elrond-egld","golem-network-tokens"]
