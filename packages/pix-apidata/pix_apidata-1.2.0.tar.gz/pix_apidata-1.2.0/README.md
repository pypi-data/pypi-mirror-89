# AccelPix Data API

# Introduction 

Python library to connect and stream the market data.
This is websocket and fallback transport based library with all the functionalyties to get eod and live streaming data

Simple and easy integration with your application, all heavy weight works are back lifted.

> ### Streaming:
1. Initialize
2. Register required callbacks
3. Do subscribe with symbols list

> ### History:
1. Initialize
2. Async call to respective methods exposed


# Installation
```bash
pip install pix-apidata 
```

# Import
```python
import asyncio
from pix_apidata import *
```

# Initialize
```python
api = apidata_lib.ApiData()

apiKey = "api-access-key" //provided by your data vendor

apiHost = "apidata.accelpix.in" //provided by your data vendor

await api.initialize(apiKey , apiHost) 

# *** IMPORTANT ***
# *** initialize(...) - wait for initialize to complete before making any other API calls.
```
# Callbacks for live streaming
### Available callbacks  

#### api.on_trade_update(on_trade)

#### api.on_best_update(on_best)

#### api.on_refs_update(on_refs)
#### api.on_srefs_update(on_srefs)

#### Trade
```python
#callback to listen for trade data
api.on_trade_update(on_trade)
def on_trade(msg):
  print(msg) # trade msg
  # to build trade object model
  t = apidata_models.Trade(msg)
  print(t.ticker , t.oi) #likewise object can be called for id, segmentId, time, price, qty, volume, kind

#response data
  {
    id: 0, 
    ticker: 'NIFTY-1', 
    segmentId: 2, 
    time: 1293704493, 
    price: 13958.6, 
    qty: 75, 
    volume: 1587975, 
    oi: 9700275,
    kind: 'T'
  } 
```

#### Best
```python 
#callback to listen for bid, ask and respective qty
api.on_best_update(on_best)
def on_best(msg):
  print(msg) # best msg
  # to build best object model
  b = apidata_models.Best(msg)
  print(b.ticker , b.bidPrice) #likewise object can be called for segmentId, kind, bidQty, askPrice, askQty, time

#response data
  {
    ticker: 'NIFTY-1', 
    segmentId: 2, 
    kind: 'B', 
    bidPrice: 13957.45, 
    bidQty: 75, 
    askPrice: 13958.8, 
    askQty: 75, 
    time: 1293704493
  }
  ```
  
### Recent change in Refs data
```python
#callback to listen for change in o, h, l, c, oi and avg data
api.on_trade_ref(on_ref)
def on_ref(msg):
  print(msg) # refs msg
  # to build refs object model 
  ref = apidata_models.Refs(msg)
  print(ref.price) #likewise object can be called for kind, ticker, segmentId

#response data
  {
    kind: 'A',
    ticker: 'NIFTY-1',
    segmentId: 2,
    price: 11781.08984375
  }
```

### Refs snapshot data
```python 
#callback to listen for o, h, l, c, oi and avg snapshot
api.on_srefs_update(on_srefs)
def on_srefs(msg):
  print(msg) # refs msg
  # to build refs snapshot object model 
  sref = apidata_models.RefsSnapshot(msg)
  print(sref.high) #likewise object can be called for kind, ticker, segmentId, open, close, high, low, avg, oi

#response data
  {
    kind: 'V', 
    ticker: 'NIFTY-1',
    segmentId: 2, 
    open: 11749.650390625, 
    close: 11681.5498046875,
    avg: 11780.8603515625,
    high: 11822,
    low: 11731.2001953125,
    oi: 10615950
  }
```

# Callbacks for connection status
### Available callbacks

#### api.on_connection_started(connection_started)

#### api.on_connection_stopped(connection_stopped)

```python
# Fired when connection is successful
def connection_started():
  print("Connection started callback")

# Fired when the connection is closed after automatic retry or some issues in networking
# Need to re-establish the connection manually

def connection_stopped():
  print("Connection stopped callback")
```

# Live stream subscription
#### Subscribe to receive ALL updates 
```python
 await api.subscribeAll('NIFTY-1')
```

#### Subscribe to receive only TRADE updates
```python
 await api.subscribeTrade(['NIFTY-1','BANKNIFTYNIFTY-1'])
```

#### Subscribe to receive only REFS and BEST updates
```python
await api.subscribeBestAndRefs(['NIFTY-1','INFY-1'])
```

# History data - Eod
```python
#*** Continues data
#params: ticker, startDate, endDate
await api.get_eod("NIFTY-1", "20200828", "20200901")

#*** Contract data
#params: underlying ticker, startDate, endDate, contractExpiryDate
await api.get_eod_contract("NIFTY", "20200828", "20200901", "20201029")

#response data
{
  td: '2020-08-28T00:00:00',
  op: 11630,
  hp: 11708,
  lp: 11617.05,
  cp: 11689.05,
  vol: 260625,
  oi: 488325
}
```
# History data - Inraday
#### Provides intra-eod bars with the time resolution in minutes (default:'5' mins) 
#### You can set minute resolution to '1', '5', '10' and so on. 
#### Custom minute resolution also supported like '3', '7' and so on.
```python
#*** Continues data
#params: ticker, startDate, endDate, resolution
await api.get_intra_eod("NIFTY-1", "20200828", "20200901", "5")

#*** Contract data
#params: underlying ticker, startDate, endDate, contractExpiryDate
await api.get_intra_eod_contract("NIFTY", "20200828", "20200901", "20201029", "5")

#response data
{
  td: '2020-08-28T09:15:00',
  op: 11630,
  hp: 11643.45,
  lp: 11630,
  cp: 11639.8,
  vol: 4575,
  oi: 440475
}
```
# History data - Ticks
Provides back log ticks from the date time specified till current live time, that is the ticks available till request hit the server.
```python
#params: ticker, fromDateTime
await api.get_back_ticks("BANKNIFTY-1", "20201016 15:00:00")

#response data
{
  td: 2020-11-16T15:00:01.000Z,
  pr: 23600,
  vol: 125,
  oi: 1692375
}
```
# Example
``` Python
import asyncio
from pix_apidata import *

api = apidata_lib.ApiData()
event_loop = asyncio.get_event_loop()

async def main():
    api.on_connection_started(connection_started)
    #api.on_connection_stopped(connection_stopped)
    api.on_trade_update(on_trade)
    #api.on_best_update(on_best)
    #api.on_refs_update(on_refs)
    #api.on_srefs_update(on_srefs)
    # key = "uA07NbY+vrg92V560rVxuVFI28Hukfco6GsblWXi7mamAvYL0as98ud4jEda+2DC"
    key = "your-api-key"
    host = "apidata.accelpix.in"
    s = await api.initialize(key, host)
    print(s)

    his = await api.get_eod_contract("NIFTY","20200828", "20200901", "20201029")
    print("History : ",his)

    syms = ['NIFTY-1', 'BANKNIFTY-1']
    await api.subscribeAll(syms)
    print("subs done")
 
 def connection_started():
    print("Connection started callback")

#def connection_stopped():
    #print("Connection stopped callback")

def on_trade(msg):
    t = apidata_models.Trade(msg)
    print(t.oi)

/'''def on_best(msg):
    b = apidata_models.Best(msg)
    print(b.bidPrice)

def on_refs(msg):
    ref = apidata_models.Refs(msg)
    print(ref.price)

def on_srefs(msg):
    sref = apidata_models.RefsSnapshot(msg)
    print(sref.high)'''/

event_loop.create_task(main())
event_loop.run_forever()

```

### Powered by ticAnalytics®
