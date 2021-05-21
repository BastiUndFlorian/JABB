import math
from datetime import datetime

class Runner:
	"""
	Runs strategies
	"""
	def __init__(self, strategy, warmup_len=0, run_live=False, data=None):
		self.strategy = strategy
		self.warmup_len = warmup_len
		self.run_live = run_live
		try:
			if not self.run_live:
				if data is not None:
					self.data = data
		except:
			print("No data was passed for a simulation run.")
			print("Try to set the run to live or pass a data.")
		self.data = data

	def run(self):
		if self.run_live:
			"""Run live strategy with websocket"""
		elif not self.run_live:
			count = 0
			for index, row in self.data.iterrows():
				timestamp = datetime.utcfromtimestamp(row["Unix Timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
				for product_id in self.strategy.product_ids:
					candle = row[product_id + "-Close"]
					if not math.isnan(candle):
						self.strategy.update(timestamp, product_id, candle)
				if count >= self.warmup_len:
					self.strategy.trade(timestamp)
				count += 1
			print("Portfolio overall value:")
			print(self.portfolio.get_portfolio_value())
			print("\n")



