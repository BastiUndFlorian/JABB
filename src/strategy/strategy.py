import numpy as np 
import itertools
import math
import time
import re
from datetime import datetime

from portfolio import Portfolio
from liveprices import WebSocket

class BaseStrategy:
	"""Create BaseClass to inherit from
		Strategy should specify:
			- buy_condition
			- quantitiy
			- profit?
			- stop-loss?
		warmup as bool or maybe as interval and count internally when warmup is done?
	"""

	def __init__(self, portfolio, is_simulation, product_ids, data=None, **kwargs):
		print("Creating strategy..")

		self.portfolio = portfolio
		self.product_ids = product_ids
		self.positions = []
		self.is_simulation = is_simulation

		if self.is_simulation:
			self.data = data
			assert self.data is not None

		self.buy_signals = None
		self.sell_signals = None

	def run(self, warmup_len=0):
		print("Running..")
		count = 0
		if self.is_simulation:
			for index, row in self.data.iterrows(): 
				# print(count)
				timestamp = datetime.utcfromtimestamp(row["Unix Timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
				for product_id in self.product_ids:
					candle = row[product_id + "-Close"]
					if not math.isnan(candle):
						self.update(product_id, candle)
						if count >= warmup_len:
							self.on_data(timestamp, candle, product_id)
				count += 1
		else:
			pass

	def start(self):
		"""Start Thread in Live position"""
		pass

	def update(self, product_id, candle):
		""" Update Portfolio/Signal """
		assets = re.split("-", product_id)
		self.portfolio.update(assets[0] + "-" + assets[1], candle)
		self.portfolio.update(assets[1] + "-" + assets[0], round(1/candle, 8))

		if self.buy_signals is not None:
			self.buy_signals[product_id].update(candle)
		if self.sell_signals is not None:
			self.sell_signals[assets[1] + "-" + assets[0]].update(round(1/candle, 8))

	def on_data(self, tme_stamp, candle, product_id):
		"""override in specific Strategy class"""
		pass


	def buy(self, tme_stamp, candle, selling_asset, buying_asset, amount):
		"""buy function"""
		if self.portfolio.holding[selling_asset] >= amount:
			#print("Opening position")
			# self.positions.append()
			print("****************************")
			print("Timestamp: " + tme_stamp + "\n")
			print("Selling " + selling_asset)
			print("Buying " + buying_asset)
			print("at Price: " + str(self.portfolio.prices[selling_asset + "-" + buying_asset]) + "\n")
			self.portfolio.from_asset_to_asset(selling_asset, buying_asset, amount)
			print("Portfolio assets:")
			print(self.portfolio.get_assets())
			print("\n")
			print("Portfolio overall value:")
			print(self.get_value())
			print("\n")	
	