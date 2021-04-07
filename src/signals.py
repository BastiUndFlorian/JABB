from indicators import MovingAverage

class MovingAverageSignal():

	def __init__(self, short_ma_window, long_ma_window, **kwargs):
		self.short_ma = MovingAverage(window_size=short_ma_window)
		self.long_ma = MovingAverage(window_size=long_ma_window)

	def check_condition(self, candle):
		#print("GETTING MOVING AVERAGE SIGNAL..\n")

		diff = 0.97     
		if diff*self.short_ma.get() > self.long_ma.get():
			return True
		else: 
			return False

	def update(self, candle):
		self.long_ma.update(candle)
		self.short_ma.update(candle)
		pass