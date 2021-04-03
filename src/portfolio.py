
import numpy as np
import itertools
import math
import itertools


class Portfolio:

	holding = {}
	# EUR or USD
	currencys = ["USD","BTC","ETH","ZEC"]

	price = {}
	

	buy_price = 0


	def __init__(self,init_value = 100):
		print("creating portfolio")

		self.holding = dict.fromkeys(self.currencys, 0)

		self.holding["USD"] = init_value

		for pair in [i + "-" + j for (i,j) in itertools.product(self.currencys, self.currencys)]:
			self.price[pair]=0
		self.price["USD-USD"]=1

		self.fee = 0.995

	def update(self, name, new_price):
		if not math.isnan(new_price):
			self.update_price(name, new_price)
			self.update_moving_average(name,new_price)
			self.run_strategy()

	def from_asset_to_asset(self, from_asset: str, to_asset: str, amount: float):
		if self.price[to_asset + '-' + from_asset] is not None and self.holding[from_asset] >= amount :
			self.holding[to_asset] += (amount * self.price[from_asset + '-' + to_asset]) * self.fee
			self.holding[from_asset] -= amount 
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
			if self.price[asset+"-USD"] is not None:
				value += self.holding[asset] * self.price[asset+"-USD"]
		return value

	def get_eur_value(self):
		return self.holding["USD"]

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


