import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('seaborn')



class MovingAverage():

	def __init__(self, window_size: int = 20):
		self._window_size = window_size
		self.window = [0]*self._window_size
		self._iter = 0
		self.ma = 0

	def update(self, price):
		self.ma += (price - self.window[self._iter])/self._window_size
		self.window[self._iter] = price
		self._iter = (self._iter + 1) % self._window_size
		pass
	def get(self):
		return self.ma


class RSIIndicator():
	'''
	The relative strength index (RSI) is a momentum indicator 
	used in technical analysis that measures the magnitude of 
	recent price changes to evaluate overbought or oversold 
	conditions in the price of a stock or other asset
	'''

	def __init__(self, close: pd.Series, window: int = 14):
		self._close = close
		self._window = window
		self._calculate_rsi()

	def _calculate_rsi(self):
		diff = self.window[self._iter] - self.price
		
		diff = self._close.diff(1)
		up_direction = diff.where(diff > 0, 0.0)
		down_direction = -diff.where(diff < 0, 0.0)
		min_periods = self._window
		emaup = up_direction.ewm(
			alpha=1 / self._window, min_periods=min_periods, adjust=False
		).mean()
		emadn = down_direction.ewm(
			alpha=1 / self._window, min_periods=min_periods, adjust=False
		).mean()
		relative_strength = emaup / emadn
		self._rsi = pd.Series(
			np.where(emadn == 0, 100, 100 - (100 / (1 + relative_strength))),
			index=self._close.index,
		)

class BollingerBands():
	'''
	Bollinger bands help determine whether prices are high or low on a relative basis. 
	They are used in pairs, both upper and lower bands and in conjunction with a moving average. 
	Further, the pair of bands is not intended to be used on its own. 
	Use the pair to confirm signals given with other indicators.

	https://www.fidelity.com/learning-center/trading-investing/
		technical-analysis/technical-indicator-guide/
			bollinger-bands#:~:text=Bollinger%20bands%20help%20determine%20whether,signals%20given%20with%20other%20indicators.
	'''
	def __init__(self, close: pd.Series, window: int = 14, window_dev: int = 2):
		self._close = close
		self._window = window
		self._window_dev = window_dev
		self._calculate_bollinger_bands()

	def _calculate_bollinger_bands(self):
		min_periods = self._window
		self._mavg = self._close.rolling(self._window, min_periods=min_periods).mean()
		self._mstd = self._close.rolling(self._window, min_periods=min_periods).std()
		self._hband = self._mavg + self._window_dev * self._mstd
		self._lband = self._mavg - self._window_dev * self._mstd
	
### This is all just Visualization needs to be somewhere else
if __name__ == '__main__':
	path = ""
	data = pd.read_csv(path, index_col=0)
	data = data[::-1]

	RSI = RSIIndicator(data["Close"], window=14*24*60)
	Bollinger = BollingerBands(data["Close"], window=14*24*60)

	plt.plot(data["Close"])
	#plt.plot(RSI._rsi, label="RSI Indicator")
	plt.plot(Bollinger._hband, label="Upper Band")
	plt.plot(Bollinger._lband, label="Lower Band")
	plt.plot()
	plt.legend()
	plt.show()


