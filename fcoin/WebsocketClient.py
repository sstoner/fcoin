import json
from websocket import create_connection
from threading import Thread
import time

class WebsocketClient():
    def __init__(self, ws_url="wss://api.fcoin.com/v2/ws", topics="ticker.ethusdt",subprotocols=["binary","base64"]):
        self.stop = False
        self.url = ws_url
        self.topics = topics
        self.thread = Thread(target=self.setup)
        self.thread.start()

    def setup(self):
        self.open()
        self.ws = create_connection(self.url)
        if type(self.topics) is list:
            subParams = json.dumps({"id": "tickers", "cmd": "sub", "args": self.topics })
        else:
            subParams = json.dumps({"id": "tickers", "cmd": "sub", "args": [self.topics]})
        self.ws.send(subParams)
        self.listen()

    def open(self):
        print("-- Subscribed! --")

    def listen(self):
        while not self.stop:
            try:
                msg = json.loads(self.ws.recv())
            except Exception as e:
                #print e
                break
            else:
                self.message(msg)

    def message(self, msg):
        #inherit method
        print(msg)

    def close(self):
        self.ws.close()
        self.closed()

    def closed(self):
        print("Socket Closed")
