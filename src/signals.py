from indicators import SimpleMovingAverage, ExponentialMovingAverage

'''
	TODO:
	Maybe Build Base class to inherit from?
	Naming convention misleading.
	Maybe putting this in a class is overkill;

'''
class BuyAndHoldSignal():
	def __init__(self, portfolio):
		self.portfolio = portfolio

	def check_condition(self, candle):
		if self.portfolio.holding[self.portfolio.default_currency] != 0.0:
			return True
		else: 
			return False
			
	def update(self, candle):
		pass

class DCASignal():
	def __init__(self, portfolio, dca_amount, interval):
		self.portfolio = portfolio
		self.dca_amount = dca_amount
		self.interval = interval
		self.time_since_last_buy = 0

	def check_condition(self, candle):
		if self.portfolio.holding[self.portfolio.default_currency] != 0.0 and self.time_since_last_buy%self.interval == 0:
			self.time_since_last_buy += 1
			return True
		else: 
			self.time_since_last_buy += 1
			return False
			
	def update(self, candle):
		pass

class SimpleMovingAverageSignal():

	def __init__(self, short_ma_window, long_ma_window, **kwargs):
		self.short_ma = SimpleMovingAverage(window_size=short_ma_window)
		self.long_ma = SimpleMovingAverage(window_size=long_ma_window)

	def check_condition(self, candle):

		diff = 0.97 
		if diff*self.short_ma.get() > self.long_ma.get():
			return True
		else: 
			return False

	def update(self, candle):
		self.long_ma.update(candle)
		self.short_ma.update(candle)
		pass

class ExponentialAverageSignal():
	def __init__(self, window_size_1, window_size_2, window_size_3, window_size_4,  **kwargs):
		self.ema_1 = ExponentialMovingAverage(window_size=window_size_1)
		self.ema_2 = ExponentialMovingAverage(window_size=window_size_2)
		self.ema_3 = ExponentialMovingAverage(window_size=window_size_3)
		self.ema_4 = ExponentialMovingAverage(window_size=window_size_4)

	def check_condition(self, candle):
		#print("GETTING MOVING AVERAGE SIGNAL..\n")
		diff = 0.97
		cond_1 = diff*self.ema_3.get() > self.ema_4.get()
		cond_2 = diff*self.ema_1.get() > self.ema_2.get()
		if cond_1 and cond_2:
			return True
		else: 
			return False
		
	def update(self, candle):
		self.ema_1.update(candle)
		self.ema_2.update(candle)
		self.ema_3.update(candle)
		self.ema_4.update(candle)
		pass