import numpy as np

import requests
import json

from datetime import datetime, timedelta,date
import pytz

import os
import pandas as pd

from portfolio import Portfolio


class DataLoader:
    tz = pytz.timezone('Europe/Berlin')
    url = "https://api.pro.coinbase.com"

    path = "./historical_data/"


    def get_historical_dataAPI(self,date_from,date_to):

        res = []
        date_from = (date_from - datetime(1970, 1, 1)).total_seconds()
        date_to = (date_to - datetime(1970, 1, 1)).total_seconds()
        for i in range(int(date_from),int(date_to),18000):

            response = requests.get(self.url + "/products/BTC-EUR/candles",params={"start": datetime.fromtimestamp(i, self.tz).isoformat(),"end": datetime.fromtimestamp(i+ 18000, self.tz).isoformat(), "granularity":60})
            # time, low, high, open, close, volume
            res += response.json()

        return res


    def load_data(self):
        
        res = pd.DataFrame(columns=["Unix Timestamp","Open","High","Low","Close","Volume"])
        filenames = [filename for filename in os.listdir(self.path) if filename.endswith('csv')]

        for filename in filenames:
            data_tmp = pd.read_csv(self.path + filename)[["Unix Timestamp","Open","High","Low","Close","Volume"]]

            data_tmp = data_tmp.reindex(index=data_tmp.index[::-1])

            res = res.append(data_tmp)

        return res.to_numpy()

if __name__ == "__main__":
    dl = DataLoader()
    pf = Portfolio()

    for stick in dl.load_data():

        pf.update("BTC",stick[4])
        if pf.ma50["BTC"] is None:
            break
        print(datetime.utcfromtimestamp(int(stick[0])).strftime('%Y-%m-%d %H:%M:%S'),pf.get_portfolio_value(),pf.ma50["BTC"],pf.ma200["BTC"])