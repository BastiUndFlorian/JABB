from signals import MovingAverageSignal
from strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):

	def __init__(self, portfolio, is_simulation, currency_list):
		super().__init__(portfolio, is_simulation, currency_list)
		self.portfolio = portfolio
		self.currency_list = currency_list

		self.buy_signals = {}
		for key in [i + "-" + j for (i,j) in itertools.product(currency_list,currency_list) if i != j]:
			self.buy_signals[key] = MovingAverageSignal(50, 200)


	def on_data(self, candle, from_asset, to_asset, warmup):
		"""
			- check buy condition
			- update the the Signal/Indicators
		"""
		self.buy_signals[from_asset + "-" + to_asset].update(candle)

		if not warmup:
			buy_condition = self.buy_signals[from_asset + "-" + to_asset].check_condition(candle)
			if buy_condition:
				self.buy(candle, from_asset, to_asset)
			else:
				pass
