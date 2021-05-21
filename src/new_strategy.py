import numpy as np 
import itertools
import re

from indicators import SimpleMovingAverage
from portfolio import Portfolio

class MovingAverageStrategy:
	"""
	"""
	def __init__(self, portfolio, currencies, **kwargs):
		print("Creating strategy..")

		self.portfolio = portfolio
		self.product_ids = []
		for product_id in [i + "-" + j for (i,j) in itertools.product(currencies, currencies) if i != j]:
			self.product_ids.append(product_id)
		print(self.product_ids)
		self.indicator_dict = self.__init_indicators()

	def __init_indicators(self):
		indicator_dict = {}
		for product_id in self.product_ids:
			indicator_dict[product_id] = [SimpleMovingAverage(50), SimpleMovingAverage(200)]
		print(indicator_dict)
		return indicator_dict

	def update(self, timestamp, product_id, candle):
		"""Update Portfolio/Signals/Indicators"""
		self.portfolio.update(product_id, candle)
		self.indicator_dict[product_id][0].update(candle)
		self.indicator_dict[product_id][1].update(candle)



	def trade(self, timestamp):
		diff = 0.97
		for product_id in self.product_ids:
			if self.indicator_dict[product_id][0].get() < diff * self.indicator_dict[product_id][1].get():
				"""Swap from asset to asset"""
				assets = re.split("-", product_id)
				amount = self.portfolio.holding[assets[1]]
				if self.portfolio.from_asset_to_asset(from_asset=assets[1], to_asset=assets[0], amount=amount) and amount > 0:
					print("****************************")
					print("Timestamp: " + timestamp + "\n")
					print("Selling " + assets[1])
					print("Buying " + assets[0])
					print("at Price: " + str(self.portfolio.prices[assets[0] + "-" + assets[1]]) + "\n")
					print("Portfolio assets:")
					print(self.portfolio.get_assets())
					print("\n")
					print("Portfolio overall value:")
					print(self.portfolio.get_portfolio_value())
					print("\n")					





