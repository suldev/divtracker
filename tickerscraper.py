import requests as client
import urllib
import time
from configuration import apikey

__debug = True

def __debug(*statements: str):
    if(__debug): print("[DEBUG]:", statements)

def all_stock_tickers() -> [str]:
    tickers = [str]
    uri = "https://api.polygon.io/v3/reference/tickers?"
    params = {'market': 'stocks', 'active': 'true', 'apikey': apikey}
    response = client.get(uri + urllib.parse.urlencode(params)).json()
    while("next_url" in response):
        for stock in response["results"]:
            tickers.append(stock["ticker"])
        response = client.get(response["next_url"] + "&apikey=" + apikey).json()
        if "count" in response:
            __debug("received a count of", response["count"], "with the lastest ticker", tickers[len(tickers) - 1])
        else:
            __debug("exceeded api requests.. waiting one minute...")
            time.sleep(60)
    return tickers

def ticker_details(ticker: str) -> dict:
    uri = "https://api.polygon.io/v3/reference/tickers/" + ticker.upper() + "?"
    params = {'apikey': apikey}
    response = client.get(uri + urllib.parse.urlencode(params))
    return response.json()

print(all_stock_tickers())