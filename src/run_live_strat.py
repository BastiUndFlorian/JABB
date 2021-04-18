from strategy.moving_average_strategy import MovingAverageStrategy
from liveprices import WebSocket
from portfolio import Portfolio
import time

# This is an experiment. Should be refined

product_ids = ["ETH-EUR", "ETH-BTC", "BTC-EUR"]

class MyWebsocketClient(WebSocket):
	def __init__(self, strategy, products):
		super().__init__(channels=["ticker"], products=products)
		self.strategy = strategy
	def on_data(self, msg):
#         print("new price.." + "\n")
		if msg["type"] == "ticker":
			timestamp = msg["time"]
			candle = float(msg["price"])
			product_id = msg["product_id"]
			self.strategy.update(product_id, candle)
			self.strategy.on_data(timestamp, candle, product_id)
		

if __name__ == '__main__':
	portfolio = Portfolio(currency_list = ["EUR", "BTC", "ETH", "ETC", "ADA"], default_currency = "EUR",init_value = 1000.0)
	MAStrat = MovingAverageStrategy(portfolio=portfolio, is_simulation=False, product_ids=product_ids)
	stuff = MyWebsocketClient(strategy=MAStrat, products=product_ids)
	print(stuff.url, stuff.products)
	stuff.start()
