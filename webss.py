import asyncio
import websockets
import json

#async def hello():
ws = websockets.connect('wss://api.bitfinex.com/ws/2')

req = json.dumps({"event": "subscribe",
       "channel": "trades",
       "symbol": 'tBTCUSD'})


ws.send(req)
print("request: > {}".format(req))


while True:
        greeting = ws.recv()
        #result = json.loads(greeting)
        print("< {}".format(result))


#asyncio.get_event_loop().run_until_complete(hello())