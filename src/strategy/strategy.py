import numpy as np 
import itertools

from portfolio import Portfolio

class BaseStrategy:
	"""Create BaseClass to inherit from
		Strategy should specify:
			- buy_condition
			- quantitiy
			- profit?
			- stop-loss?
		warmup as bool or maybe as interval and count internally when warmup is done?
	"""

	def __init__(self, portfolio, is_simulation, currency_list, **kwargs):
		print("Creating strategy..")

		self.portfolio = portfolio
		self.currency_list = currency_list
		self.positions = []
		self.is_simulation = is_simulation
		self.buy_signals = {}

	def start(self):
		"""Start Thread in Live position"""
		pass

	def update(self, candle, from_asset, to_asset, warmup=False):
		"""Update Candle/Indicators/Signals/Portfolio"""
		self.portfolio.update(from_asset + "-" + to_asset, candle)
		self.on_data(candle, from_asset, to_asset, warmup)

	def on_data(self, candle, from_asset, to_asset):
		"""override in specific Strategy class"""
		pass


	def buy(self, candle, from_asset, to_asset):
		"""quantitiy?
			profit?
			stop-loss?
		"""
		if self.portfolio.holding[from_asset] != 0.0:
			#print("Opening position")
			# self.positions.append()
			print("****************************")
			print("Selling " + from_asset)
			print("Buying " + to_asset + "\n")
			self.portfolio.from_asset_to_asset(from_asset, to_asset, self.portfolio.holding[from_asset])
			print("Portfolio assets: \n")
			print(self.portfolio.get_assets())
			print("\n")


	def get_value(self):
		return self.portfolio.get_portfolio_value()




	
	