import itertools
import re

from signals import BuyAndHoldSignal
from strategy import BaseStrategy


class BuyAndHoldStrategy(BaseStrategy):

	def __init__(self, portfolio, is_simulation, product_ids, curr_to_hold, data=None):
		super().__init__(portfolio, is_simulation, product_ids, data)
		self.portfolio = portfolio
		self.curr_to_hold = curr_to_hold
		self.buy_signals = {}
		self.buy_signals[self.portfolio.default_currency + "-" + self.curr_to_hold] = BuyAndHoldSignal(self.portfolio)

	def on_data(self, tme_stamp, candle, product_id):
		"""
			- check buy condition
			- update the the Signal/Indicators
		"""
		#self.buy_signals[from_asset + "-" + to_asset].update(candle)
		assets = re.split("-", product_id)

		if assets[0] == self.portfolio.default_currency and assets[1] == self.curr_to_hold:
			buy_condition = self.buy_signals[product_id].check_condition(candle)
			if buy_condition:
				self.buy(tme_stamp, candle, assets[0], assets[1], self.portfolio.holding[assets[0]])
