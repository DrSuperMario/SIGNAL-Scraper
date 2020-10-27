URL = ("https://www.tradingview.com/markets/currencies/rates-all/",
       "https://coinmarketcap.com/",
       "https://www.hl.co.uk/shares/stock-market-news",
       "https://www.ft.com/news-feed",
       "https://finviz.com/news.ashx",
       "https://www.coingecko.com/en/coins/all")

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
    "NAME": "d-none d-lg-block font-bold",
    "PRICE": "no-wrap",
    "PRICE_CAP": "Text-sc-1eb5slv-0 hVAibX",
                 "VOLUME_24": "Text-sc-1eb5slv-0 iOrfwG font_weight_500___2Lmmi",
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

fixedCoinList = ['bitcoin',
                 'ethereum',
                 'tether',
                 'xrp',
                 'bitcoin-cash',
                 'chainlink',
                 'binance-coin',
                 'polkadot-new',
                 'litecoin',
                 'bitcoin-sv',
                 'cardano',
                 'usd-coin',
                 'eos',
                 'monero',
                 'crypto-com-coin',
                 'tron',
                 'stellar',
                 'tezos',
                 'wrapped-bitcoin',
                 'unus-sed-leo',
                 'neo',
                 'cosmos',
                 'multi-collateral-dai',
                 'huobi-token',
                 'nem',
                 'filecoin',
                 'iota',
                 'binance-usd',
                 'vechain',
                 'dash',
                 'theta',
                 'ethereum-classic',
                 'zcash',
                 'uniswap',
                 'maker',
                 'omg',
                 'compound',
                 'uma',
                 'yearn-finance',
                 'ontology',
                 'aave',
                 'ftx-token',
                 'synthetix-network-token',
                 'dogecoin',
                 'abbc-coin',
                 'waves',
                 'algorand',
                 'basic-attention-token',
                 'bittorrent',
                 'celsius',
                 'kusama',
                 'okb',
                 'digibyte',
                 'trueusd',
                 '0x',
                 'ren',
                 'husd',
                 'paxos-standard',
                 'celo',
                 'hedgetrade',
                 'qtum',
                 'icon',
                 'zilliqa',
                 'energy-web-token',
                 'ocean-protocol',
                 'kyber-network',
                 'hedera-hashgraph',
                 'quant',
                 'loopring',
                 'flexacoin',
                 'nxm',
                 'decred',
                 'reserve-rights',
                 'augur',
                 'lisk',
                 'near-protocol',
                 'bitcoin-gold',
                 'cybervein',
                 'zb-token',
                 'terra-luna',
                 'revain',
                 'ampleforth',
                 'siacoin',
                 'band-protocol',
                 'elrond-egld',
                 'enjin-coin',
                 'the-midas-touch-gold',
                 'nano',
                 'aragon',
                 'decentraland',
                 'avalanche',
                 'blockstack',
                 'sushiswap',
                 'bitcoin-diamond',
                 'velas',
                 'numeraire',
                 'orchid',
                 'golem-network-tokens',
                 'arweave',
                 'monacoin']
