import requests as client
import urllib
import time
from configuration import apikey

__debug = True
def __debug(*statements: str):
    if(__debug): print("[DEBUG]:", ' '.join(statements))


currentStock = 0
totalStocks = 0
params = {'market': 'stocks', 'active': 'true', 'apikey': apikey}
tickerStack = client.get("https://api.polygon.io/v3/reference/tickers?" + urllib.parse.urlencode(params)).json()
if(tickerStack["status"] == "ERROR"):
    print(tickerStack["error"])
    quit()
while("next_url" in tickerStack): #scroll through the pages
    if "count" in tickerStack:
        __debug("read", str(tickerStack["count"]), "tickers...")
        totalStocks += len(tickerStack["results"])
        for ticker in tickerStack["results"]:
            currentStock += 1
            __debug(f"[{currentStock}/{totalStocks}]:", "fetching data from", ticker["ticker"])
            desc = client.get("https://api.polygon.io/v3/reference/tickers/" + ticker["ticker"] + "?apikey=" + apikey).json()
            if desc["status"] == "ERROR":
                __debug("API calls exceeded... waiting one minute...")
                time.sleep(60)
                desc = client.get("https://api.polygon.io/v3/reference/tickers/" + ticker["ticker"] + "?apikey=" + apikey).json()
            #TODO: write data to mariadb
    else:
        __debug("API calls exceeded... waiting one minute...")
        time.sleep(60)