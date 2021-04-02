
import numpy as np

import math


class Portfolio:

	holding = {}
	
	currencys = ["USD","BTC","ETH","ZEC"]

	price = {}

	ma50 = {
		"EUR":0,
		"BTC":0,
		"ETH":0,
		"LTC":0
	}

	ma200 = {
		"EUR":0,
		"BTC":0,
		"ETH":0,
		"LTC":0
	}

	ma50_cache =  {
		"EUR":[0] * 50,
		"BTC":[0] * 50,
		"ETH":[0] * 50,
		"LTC":[0] * 50
	}

	ma200_cache =  {
		"EUR":[0] * 200,
		"BTC":[0] * 200,
		"ETH":[0] * 200,
		"LTC":[0] * 200
	}

	ma50_iter = {
		"EUR":0,
		"BTC":0,
		"ETH":0,
		"LTC":0
	}

	ma200_iter = {
		"EUR":0,
		"BTC":0,
		"ETH":0,
		"LTC":0
	}

	buy_price = 0


	def __init__(self,init_value = 100):
		print("creating portfolio")

		self.holding = dict.fromkeys(currencys)

		self.holding["EUR"] = init_value

		for pair in [i + "-" + j for (i,j) in itertools.product(self.currencys, self.currencys) if i != j]:
			self.price[pair]=None

		self.phi = 0.995

	def update(self, name, new_price):
		if not math.isnan(new_price):
			self.update_price(name, new_price)
			self.update_moving_average(name,new_price)
			self.run_strategy()

	def from_asset_to_asset(self, from_asset: str, to_asset: str, amount: float):
		# TODO: check if holdings cover the amount
		price_from_asset = self.price[from_asset]
		price_to_asset = self.price[to_asset]
		if self.price[to_asset] is not None:
			self.holding[to_asset] += (amount / self.price[from_asset + '-' + to_asset]) * self.phi
			self.holding[from_asset] -= (amount / self.price[to_asset + '-' + from_asset]) * self.phi
			return True
		else:
			return False
		
	def buy_in_eur(self,name, amount):
		if self.price[name] is not None  and amount <= self.holding["EUR"]:
			self.holding[name] += (amount / self.price[name])*0.995
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

	def sell_in_asset(self, name, amount):
		if self.price[name] is not None and amount <= self.holding[name]:
			self.holding["EUR"] += (amount * self.price[name])*0.995
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

    def run_strategy(self):
        
        diff = 0.97

        if diff*(self.ma50["BTC"]) > self.ma200["BTC"]:
            self.sell_in_asset("BTC",self.holding["BTC"])        
        if self.ma50["BTC"] < diff*(self.ma200["BTC"]):
            self.buy_price = self.price["BTC"]
            self.buy_in_eur("BTC",self.holding["EUR"])
        pass

	def update_moving_average(self,name,price):  
		
		self.ma50[name] += (price - self.ma50_cache[name][self.ma50_iter[name]])/50
		self.ma50_cache[name][self.ma50_iter[name]] = price
		self.ma50_iter[name] = (self.ma50_iter[name] + 1) % 50

		self.ma200[name] += (price - self.ma200_cache[name][self.ma200_iter[name]])/200
		self.ma200_cache[name][self.ma200_iter[name]] = price
		self.ma200_iter[name] = (self.ma200_iter[name] + 1) % 200

		pass

if __name__ == "__main__":
	
	pf = Portfolio()


