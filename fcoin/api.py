import requests
from .auth import HMACAuth
import collections
import json
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
