import numpy as np
import requests
from datetime import datetime
import pytz
import pandas as pd
import itertools



class DataLoader:
    tz = pytz.timezone('Europe/Berlin')
    url = "https://api.pro.coinbase.com"

    path = "C:/Users/flori/Contacts/Documents/Git_Repos/JABB/historical_data/"


    def get_historical_dataAPI(self,date_from,date_to):

        res = []
        date_from = (date_from - datetime(1970, 1, 1)).total_seconds()
        date_to = (date_to - datetime(1970, 1, 1)).total_seconds()
        for i in range(int(date_from),int(date_to),18000):

            response = requests.get(self.url + "/products/BTC-EUR/candles",params={"start": datetime.fromtimestamp(i, self.tz).isoformat(),"end": datetime.fromtimestamp(i+ 18000, self.tz).isoformat(), "granularity":60})
            # time, low, high, open, close, volume
            print(response.json())
            res += list(response.json()).reverse() # todo reverse not working

        return res

    def load_data(self,date_from,date_to):


        date_from = (date_from - datetime(1970, 1, 1)).total_seconds()
        date_to = (date_to - datetime(1970, 1, 1)).total_seconds()

        '''if date_from < (datetime(2019, 1, 1) - datetime(1970, 1, 1)).total_seconds():
            print("no data for dates before 2019-01-01")
            return

        if date_to > (datetime(2020, 12, 31) - datetime(1970, 1, 1)).total_seconds():
            print("no data for dates after 2020-12-31")
            return'''
        

        years = [2019,2020]
        currencys = ["USD","BTC","ETH","ZEC"]

        print([i + "-" + j for (i,j) in itertools.product(currencys,currencys) if i != j])

        df = pd.DataFrame(columns=["Unix Timestamp"])

        for i in range(0,len(currencys)):
            for j in range(0,len(currencys)):
                if j < i:
                    df_tmp = pd.DataFrame(columns=["Unix Timestamp",currencys[i]+ "-" +  currencys[j] + "-Close"])
                    for year in years:
                        
                        print("loading gemini_" + currencys[i] + currencys[j] + "_" + str(year) + "_1min.csv")
                        data_tmp = pd.read_csv(self.path + "gemini_" + currencys[i] + currencys[j] + "_" + str(year) + "_1min.csv",skiprows=1)[["Unix Timestamp","Close"]]
                        data_tmp = data_tmp.rename(columns={"Close":currencys[i]+ "-" +  currencys[j] + "-Close"})
                        data_tmp[currencys[j]+ "-" +  currencys[i] + "-Close"] = 1/data_tmp[currencys[i]+ "-" +  currencys[j] + "-Close"]
                        data_tmp = data_tmp.reindex(index=data_tmp.index[::-1])
                        df_tmp = df_tmp.append(data_tmp)
                    if df.empty:
                        df = df_tmp
                    else:
                        df = df.join(df_tmp.set_index('Unix Timestamp'), lsuffix='', rsuffix='_other',on="Unix Timestamp")

        df['Unix Timestamp'] = df['Unix Timestamp'] // 1000
        df = df[df['Unix Timestamp'] >= date_from]
        df = df[df['Unix Timestamp'] <= date_to]
        return df




if __name__ == "__main__":
    dl = DataLoader()
    res = dl.load_data(datetime(2019, 1, 1),datetime(2020, 12, 31))
    print(res)