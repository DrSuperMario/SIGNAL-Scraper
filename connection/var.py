URL = ("https://www.tradingview.com/markets/currencies/rates-all/", "https://coinmarketcap.com/")

parser = "html.parser"

agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

agent_smartphone = 'Mozilla/5.0 (Linux; Android 9; SM-G960F '\
'Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) '\
'Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'

agent_old_smartphone = 'Mozilla/5.0 (Linux; Android 9; SM-G960F '\
'Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) '\
'Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'

ConnectionVar_crypto = {
                 "NAME":"cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name",
                 "PRICE":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price",
                 "PRICE_CAP":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap",
                 "VOLUME_24":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h",
                 "CIRCULATION":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply",
                 "PERCENT_CHG":"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h"
}

ConnectionVar_forex = {
                "NAME":"tv-screener__symbol apply-common-tooltip",
                "PRICE":"tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big tv-screener-table__cell--with-marker tv-screener-table__cell--highlighted"

}