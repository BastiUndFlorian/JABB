
import numpy as np
import itertools
import math


class Portfolio:

	holding = {}
	prices = {}

	def __init__(self,currency_list = ["USD","BTC","ETH","ZEC"], default_currency = "USD",init_value = 100):
		print("creating portfolio")

		self.currencys = currency_list
		self.default_currency = default_currency

		self.holding = dict.fromkeys(self.currencys, 0)
		self.holding[self.default_currency] = init_value

		for pair in [i + "-" + j for (i,j) in itertools.product(self.currencys, self.currencys)]:
			self.prices[pair]=0
		self.prices[self.default_currency + "-" +  self.default_currency]=1

		self.fee = 0.995

	def update(self, name, new_price):
		if not math.isnan(new_price):
			self.update_price(name, new_price)
			# self.update_moving_average(name,new_price)
			# self.run_strategy()

	def from_asset_to_asset(self, from_asset: str, to_asset: str, amount: float):
		if self.prices[to_asset + '-' + from_asset] is not None and self.holding[from_asset] >= amount :
			self.holding[to_asset] += (amount * self.prices[from_asset + '-' + to_asset]) * self.fee
			self.holding[from_asset] -= amount 
			return True
		else:
			return False
				
	def update_price(self, name, new_price):
		self.prices[name] = new_price
		pass

	def get_assets(self):
		return self.holding

	def get_portfolio_value(self):
		value = 0
		for asset in self.holding.keys():
			if self.prices[asset + "-" + self.default_currency] is not None:
				value += self.holding[asset] * self.prices[asset + "-" + self.default_currency]
		return value


