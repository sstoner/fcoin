import requests
from .auth import HMACAuth
import collections
import json
from .WebsocketClient import WebsocketClient
class Api():
  def __init__(self):
    self.session = requests.session()

  def _build_auth_session(self,auth):
    self.session.auth = auth

  def authorize(self,api_key,api_secret):
    auth = HMACAuth(api_key,api_secret)
    self._build_auth_session(auth)
    return self


  @property
  def accounts_balance(self):
    api_url = "https://api.fcoin.com/v2/accounts/balance"
    return self.session.get(api_url).json()
  @property
  def orders(self):
    return Orders(self.session)
  @property
  def market(self):
    return Market(self.session)

  #public api
  def currencies(self):
    self.api_url = "https://api.fcoin.com/v2/public/currencies"
    return self.session.get(self.api_url).json()

  def symbols(self):
    self.api_url = "https://api.fcoin.com/v2/public/symbols"
    return self.session.get(self.api_url).json()
  def server_time(self):
    self.api_url = "https://api.fcoin.com/v2/public/server-time"
    return self.session.get(self.api_url).json()

class Orders():
  def __init__(self,session):
    self.api_base_url = "https://api.fcoin.com/v2/orders"
    self.session = session
    pass

  def get(self,*args):
    if len(args) == 1:
      order_id = args[0]
      self.api_url = self.api_base_url + "/" + order_id
      return self.session.get(self.api_url).json()
    else:
      data = {
          "symbol": args[0] if args else "ethusdt",
          "states": args[1] if args[1:] else "submitted",
          "before": args[2] if args[2:] else "",
          "after": args[3] if args[3:] else "",
          "limit": args[4] if args[4:] else ""
          }
      sorted_params = collections.OrderedDict(sorted(data.items()))
      params = ""
      for item in sorted_params.items():
        param = item[0] + '=' + item[1]
        params = params + param + "&"
      self.api_url = self.api_base_url + "?" + params[:-1]
    return self.session.get(self.api_url).json()

  def match_results(self,order_id):
    self.api_url = self.api_base_url + "/" + "{order_id}/match-results"
    return self.session.get(self.api_url.format(order_id = order_id)).json()

  def create(self,sorted_param):
    params = ""
    for item in sorted_param.items():
      param = item[0] + '=' + item[1]
      params = params + param + "&"
    self.api_url = self.api_base_url + "?" + params[:-1]

    r =  self.session.post(self.api_url,json = sorted_param)
    return r.json()

  def submit_cancel(self,order_id):
    cancel_api_url = "https://api.fcoin.com/v2/orders/{order_id}/submit-cancel"
    return self.session.post(cancel_api_url.format(order_id=order_id)).json()


class Market():
  def __init__(self,session):
    self.session = session
    self.api_base_url = "https://api.fcoin.com/v2/market"
    self.wss_url = "wss://api.fcoin.com/v2/ws"
  def get_ticker(self,ticker):
    self.api_url = self.api_base_url + "/ticker/{ticker}".format(ticker = ticker)
    print(self.api_url)
    return self.session.get(self.api_url).json()
  def get_depth(self,level,symbol):
    self.api_url = self.api_base_url + "/depth/{level}/{symbol}".format(level=level,symbol=symbol)
    return self.session.get(self.api_url).json()

  def get_lastest_trade(self,symbol):
    self.api_url = self.api_base_url + "/trades/{symbol}".format(symbol=symbol)
    return self.session.get(self.api_url,params = {"before": "100","limit": "20"}).json()

  def get_candle_info(self,resolution,symbol):
    self.api_url = self.api_base_url + "/candles/{resolution}/{symbol}".format(resolution=resolution,symbol=symbol)
    return self.session.get(self.api_url,params = {"before": "100","limit": 20}).json()



def order_create_param(*args):
  payload = {
      "symbol": args[0],
      "side": args[1],
      "type": args[2],
      "price": args[3],
      "amount": args[4]
    }
  return collections.OrderedDict(sorted(payload.items()))

def authorize(api_key,api_secret):
  return Api().authorize(api_key,api_secret)


class HandleWS(WebsocketClient):
    pass

def init_ws():
  ws = HandleTickerWS()
  return ws




