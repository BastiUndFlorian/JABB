import numpy as np

import requests
import json

from datetime import datetime, timedelta,date
import pytz

from portfolio import Portfolio


tz = pytz.timezone('Europe/Berlin')
url = "https://api.pro.coinbase.com"

def get_historical_data(date_from,date_to):

    res = []
    date_from = (date_from - datetime(1970, 1, 1)).total_seconds()
    date_to = (date_to - datetime(1970, 1, 1)).total_seconds()
    for i in range(int(date_from),int(date_to),18000):

        response = requests.get(url + "/products/BTC-EUR/candles",params={"start": datetime.fromtimestamp(i, tz).isoformat(),"end": datetime.fromtimestamp(i+ 18000, tz).isoformat(), "granularity":60})
        # time, low, high, open, close, volume
        res.append(response.json())

    return response.json()

def run_test_enviroment(hist_data):
    pf = Portfolio()
    pf.update_price("BTC",46594.16)
    pf.buy_in_eur("BTC",100)
    for stick in hist_data:
        pf.update_price("BTC",stick[4])
        print(pf.get_portfolio_value())


run_test_enviroment(get_historical_data(datetime(2021,3,10),datetime(2021,3,11)))


#print(get_historical_data(datetime(2021,3,10),datetime(2021,3,11)))
