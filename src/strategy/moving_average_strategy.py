import itertools
import re

from signals import SimpleMovingAverageSignal
from strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):

	def __init__(self, portfolio, is_simulation, product_ids, data=None):
		super().__init__(portfolio, is_simulation, product_ids, data)
		self.portfolio = portfolio
		self.product_ids = product_ids
		self.buy_signals = {}
		self.sell_signals = {}

		for product_id in self.product_ids:
			assets = re.split("-", product_id)
			self.buy_signals[product_id] = SimpleMovingAverageSignal(50, 200)
			self.sell_signals[assets[1] + "-" + assets[0]] = SimpleMovingAverageSignal(50, 200)


	def on_data(self, tme_stamp, candle, product_id):
		"""
			- check buy condition
			- update the the Signal/Indicators
		"""
		assets = re.split("-", product_id)

		buy_condition = self.buy_signals[product_id].check_condition(candle)
		sell_condition = self.sell_signals[assets[1] + "-" + assets[0]].check_condition(round(1/candle, 8))
		if buy_condition:
			self.buy(tme_stamp, candle, assets[0], assets[1], self.portfolio.holding[assets[0]])
		elif sell_condition:
			self.buy(tme_stamp, candle, assets[1], assets[0], self.portfolio.holding[assets[1]])
		else:
			pass
