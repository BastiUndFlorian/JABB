
import numpy as np




class Portfolio:

    holding = {
        "EUR":0,
        "BTC":0,
        "ETH":0,
        "LTC":0
        }
    
    price = {
        "EUR":1,
        "BTC":None,
        "ETH":None,
        "LTC":None
    }

    ma50 = 0
    ma200 = 0

    def __init__(self,init_value = 100):
        print("creating portfolio")

        self.holding["EUR"] = init_value


    def buy_in_eur(self,name, amount):
        if self.price[name] is not None  and amount <= self.holding["EUR"]:
            self.holding[name] += amount / self.price[name]
            self.holding["EUR"] -= amount
            return True
        else:
            return False

    def sell_in_eur(self,name,amount):
        if self.price[name] is not None and amount/ self.price[name] <= self.holding[name]:
            self.holding["EUR"] += amount
            self.holding[name] -=  amount/ self.price[name] 
            return True
        else: 
            return False

    def buy_in_asset(self,name, amount):
        if self.price[name] is not None  and amount * self.price[name] <= self.holding["EUR"]:
            self.holding[name] += amount 
            self.holding["EUR"] -= amount * self.price[name]
            return True
        else: 
            return False

    def sell_in_asset(self,name,amount):
        if self.price[name] is not None and amount <= self.holding[name]:
            self.holding["EUR"] += amount * self.price[name]
            self.holding[name] -= amount
            return True
        else: 
            return False

    def update_price(self, name, new_price):
        self.price[name] = new_price
        self.update_moving_average(new_price)
        self.run_strategy()
        print(self.get_assets())
        print(self.ma200,self.ma50)
        pass

    def get_assets(self):
        return self.holding

    def get_portfolio_value(self):
        value = 0
        for asset in self.holding.keys():
            if self.price[asset] is not None:
                value += self.holding[asset] * self.price[asset]
        return value

    def get_eur_value(self):
        return self.holding["EUR"]

    def run_strategy(self):
        
        if self.ma50 > self.ma200:
            self.sell_in_asset("BTC",self.holding["BTC"])
        
        if self.ma50 < self.ma200:
            self.buy_in_eur("BTC",self.holding["EUR"])
        pass

    def update_moving_average(self,price):        
        #self.ma50 += (price - self.ma50)/50
        
        #self.ma200 += (price - self.ma200)/200

        # momentum 
        self.ma200 = price*(1/200) + (199/200)* self.ma200
        self.ma50 = price*(1/50) + (49/50)* self.ma50

        pass

if __name__ == "__main__":
    
    pf = Portfolio()

