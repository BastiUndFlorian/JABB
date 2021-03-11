
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


if __name__ == "__main__":
    
    pf = Portfolio()
    

