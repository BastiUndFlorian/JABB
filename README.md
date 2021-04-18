# JABB

1. Fully working testing enviroment
	live prices
	buy - sell - portfolio simulation
	vis

2. Strategy

3. Coinbase api (buy - sell)


## Prequisites
In order to run the DataLoader class it is neccessary to download the data from https://www.cryptodatadownload.com/data/gemini/ and save it in ./historical_data

## TODO

1. Clean Portfolio
2. Strategy class
3. VisualizaTION
4. Write Indicatorclass with subclasses (with update and get methods) as different indicators

## How to create a Strategy

1. Build the appropriate Indicator
2. Build a Signal from the Indicator to determine when to buy and sell
3. Inherit from BaseStrategy class in strategy.py and specify the on_data() function to build the corresponding strategy


### Example
1. For a simple moving average strategy we would need the SMA Indicator:
```python
class SMA():

	def __init__(self, window_size: int = 20):
		self._window_size = window_size
		self._iter = 0
		self.window = [0]*self._window_size
		self.sma = 0

	def update(self, price: float):
		self.sma += (price - self.window[self._iter])/self._window_size
		self.window[self._iter] = price
		self._iter = (self._iter + 1) % self._window_size
		pass
		
	def get(self):
		return self.sma
```
where we need to specify an update function for our indicator.

2. Then would build a corresponding signal with a check_condition() function returning True if the buy condition is met.
```python
class SMASignal():

	def __init__(self, short_ma_window, long_ma_window):
		self.short_ma = SMA(window_size=short_ma_window)
		self.long_ma = SMA(window_size=long_ma_window)

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
```
here we also need to specify an update function.
3. Lastly we can build our strategy specifying the on_data() function and initialising the indicators.
```python
from strategy.strategy import BaseStrategy
from signal import SMASignal


class SMAStrategy(BaseStrategy):

	def __init__(self, portfolio, is_simulation, product_ids, data=None):
		super().__init__(portfolio, is_simulation, product_ids, data)
		self.portfolio = portfolio
		self.product_ids = product_ids
		self.buy_signals = {}
		self.sell_signals = {}

		for product_id in self.product_ids:
			assets = re.split("-", product_id)
			self.buy_signals[product_id] = SMASignal(50, 200) # init buysignals
			self.sell_signals[assets[1] + "-" + assets[0]] = SMASignal(50, 200) # init sellsignals


	def on_data(self, tme_stamp, candle, product_id):

		assets = re.split("-", product_id)

		buy_condition = self.buy_signals[product_id].check_condition(candle) #check buy condition 
		sell_condition = self.sell_signals[assets[1] + "-" + assets[0]].check_condition(round(1/candle, 8)) #check sell condition 
		if buy_condition:
			self.buy(tme_stamp, candle, assets[0], assets[1], self.portfolio.holding[assets[0]])
		elif sell_condition:
			self.buy(tme_stamp, candle, assets[1], assets[0], self.portfolio.holding[assets[1]])
		else:
			pass
```
