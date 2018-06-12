import base64
import hmac
import hashlib
import requests
from requests.auth import AuthBase
from requests.utils import to_native_string
import time
import collections
import json

class HMACAuth(AuthBase):
    def __init__(self,api_key,api_secret,api_version="v2"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_version = api_version
    def __call__(self,request):
        timestamp = str(int(round(time.time() * 1000)))

        if request.method == "POST" and request.body:
            adjusted_body = ""
            request_body = json.loads(request.body.decode())
            request_body = collections.OrderedDict(sorted(request_body.items()))
            for item in request_body.items():
                param = item[0] + "=" + item[1]
                adjusted_body = adjusted_body + param + "&"
            message = request.method + request.url + timestamp + (adjusted_body[:-1] or "")
        elif request.method == "GET":
            message = request.method + request.url + timestamp + ""
        else:
            message = request.method + request.url + timestamp + ""

        secret = self.api_secret
        if not isinstance(message,bytes):
            message = message.encode()
        if not isinstance(secret,bytes):
            secret = secret.encode()

        b64message = base64.b64encode(message)

        if not isinstance(b64message,bytes):
            b64message = b64message.encode()

        signature = hmac.new(secret,b64message,hashlib.sha1).digest()
        if not isinstance(signature,bytes):
            signature = signature.encode()
        b64signature = base64.b64encode(signature)
        request.headers.update({
                to_native_string('FC-ACCESS-KEY'): self.api_key.encode(),
                to_native_string('FC-ACCESS-SIGNATURE'): b64signature,
                to_native_string('FC-ACCESS-TIMESTAMP'): timestamp,
            })
        return request

