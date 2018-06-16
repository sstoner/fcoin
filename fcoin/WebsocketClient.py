import json
from websocket import create_connection
from threading import Thread
import time

class WebsocketClient():
    def __init__(self, ws_url="wss://api.fcoin.com/v2/ws",subprotocols=["binary","base64"]):
        self.stop = False
        self.url = ws_url
        self.ws = create_connection(self.url)

    def sub(self,topics):
        self.open()
        subParams = json.dumps(topics)
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
                self.handle(msg)

    def handle(self, msg):
        #inherit method
        print(msg)

    def close(self):
        self.ws.close()
        self.closed()

    def closed(self):
        print("Socket Closed")
