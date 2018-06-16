# fcoin



## How to use: 
> call like what official docs do


```  
import fcoin      

api = fcoin.authorize(key,secret)  
api.accounts_balance  
```
response:  

```
{
  "status": 0,
  "data": [
    {
      "currency": "btc",
      "available": "50.0",
      "frozen": "50.0",
      "balance": "100.0"
    }
  ]
}
```
----
```
import fcoin

api = fcoin.authorize('key', 'secret', timestamp)
order_create_param = fcoin.order_create_param('btcusdt', 'buy', 'limit', '8000.0', '1.0')
api.orders.create(order_create_param)

```
response:  
```
{  
  "status": 0,  
  "data": "9d17a03b852e48c0b3920c7412867623"
}
```    

---    

> websocket client
  
```
import fcoin
from fcoin.WebsocketClient import WebsocketClient
from threading import Thread
class HandleWebsocket(WebsocketClient):
    def handle(self,msg):
        for key,value in msg.items():
            print(key,value)
ws = HandleWebsocket()
topics = {
         "id": "tickers",
         "cmd": "sub",
         "args": ["depth.L20.ethusdt"],
    }
sub = ws.sub
Thread(target=sub,args=(topics,)).start()
time.sleep(10)
ws.close()

```






