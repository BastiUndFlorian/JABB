import json
import sys
import time
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
from portfolio import Portfolio



class WebSocket():
	"""
	Handle all the real time data
	param url : websocket url string
	param api_key: personal api key
	param api_secret: secret key
	param api_passphrase: secret passphrase
	param products: products
	param channels: Channel options: ['ticker', 'user', 'matches', 'level2', 'full']
	"""
	def __init__(self, 
			url="wss://ws-feed.pro.coinbase.com",
			api_key="",
			api_secret="",
			api_passphrase="",
			products=None,
			should_print=True,
			portfolio=None,
			*,
			channels):

		self.url = url
		self.api_key = api_key
		self.api_secret = api_secret
		self.api_passphrase = api_passphrase
		self.products = products
		self.channels = channels
		self.should_print = should_print
		self.portfolio = portfolio
		self.ws = None
		self.error = None
		self.stop = True
		self.thread = None
		self.data = ""

	def _connect(self):
		if self.products is None:
			self.products = ["BTC-EUR"]
		elif not isinstance(self.products, list):
			self.products = [self.products]

		if self.url[-1] == "/":
			self.url = self.url[:-1]

		if self.channels is None:
			self.channels = [{"name": "ticker", "product_ids": [product_id for product_id in self.products]}]
			sub_params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}
		else:
			sub_params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}

		# if self.auth:
  #           timestamp = str(time.time())
  #           message = timestamp + 'GET' + '/users/self/verify'
  #           auth_headers = get_auth_headers(timestamp, message, self.api_key, self.api_secret, self.api_passphrase)
  #           sub_params['signature'] = auth_headers['CB-ACCESS-SIGN']
  #           sub_params['key'] = auth_headers['CB-ACCESS-KEY']
  #           sub_params['passphrase'] = auth_headers['CB-ACCESS-PASSPHRASE']
  #           sub_params['timestamp'] = auth_headers['CB-ACCESS-TIMESTAMP']
		self.ws = create_connection(self.url)

		self.ws.send(json.dumps(sub_params))

	def _keepalive(self, interval=30):
		while self.ws.connected:
			self.ws.ping("keepalive")
			time.sleep(interval)

	def _listen(self):
		self.keepalive.start()
		count = 0
		while not self.stop:
			try:
				data = self.ws.recv()
				msg = json.loads(data)
			except ValueError as e:
				self.on_error(e)
			except Exception as e:
				self.on_error(e)
			else:
				self.on_data(msg)

	def _disconnect(self):
		try:
			if self.ws:
				self.ws.close()
		except WebSocketConnectionClosedException as e:
			pass
		finally:
			self.keepalive.join()

		self.on_close()

	def close(self):
		self.stop = True
		self._disconnect()
		self.thread.join()

	def on_open(self):
		if self.should_print:
			print("-- Subscribed! --\n")

	def on_close(self):
		if self.should_print:
			print("-- Socket Closed! --")

	def on_data(self, msg):
		pass

	def on_error(self, e, data=None):
		self.error = e
		self.stop = True
		print("{} - data: {}".format(e, data))

	def _go(self):
		self._connect()
		self._listen()
		self._disconnect()

	def start(self):
		self.stop = False
		self.on_open()
		self.thread = Thread(target=self._go)
		self.keepalive = Thread(target=self._keepalive)
		self.thread.start()

