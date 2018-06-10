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





