import requests
import json
import datetime
import pandas as pd
import time

url="http://fx-trading-game-leicester-challenge.westeurope.azurecontainer.io:443/"
Trader_ID="gKNKsiQiRXKscOjz7DP54PSKN7bqJ4Yj"
portfolio=1000000
brexit="16:50"
Market_Open="16:30"
Bounce="17:10"
close="17:30"






def get_price():
    api_url = url + "/price/EURGBP"
    res = requests.get(api_url)
    if res.status_code == 200:
        price=json.loads(res.content.decode('utf-8'))["price"]
        print("price-->",price)

        return price
    return None

#print("Expected to trade at ",get_price())

points=[]
# for i in range(0,10):
#     price=get_price()
#     points.append(price)
# print(points)

while datetime.datetime.now() != "1650":
    price=get_price()
    points.append(price)
    df=pd.DataFrame(points,columns=["price"])
    df['EMA'] = df['price'].ewm(span=10, adjust=False).mean()
    df['signal'] = 0
    df.loc[df['price'] > df['EMA'], 'signal'] = 1  # Buy signal
    df.loc[df['price'] < df['EMA'], 'signal'] = -1  # Sell signal
    time.sleep(1)
    print("signal",df["signal"])
    if df["signal"].all() == 1:
        print("Buy")
    else:
        print("sell")
   


if all(points[i] <= points[i + 1] for i in range(len(points) - 1)):
    print("buy")
    print(all(points[i] <= points[i + 1] for i in range(len(points) - 1)))
else:
    print(all(points[i] <= points[i + 1] for i in range(len(points) - 1)))
    print("no")



previous=[get_price()]
print("Previous-->",previous)




def trade(trader_id, qty, side):
    api_url = url + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        if resp_json["success"]:
            return resp_json["price"]
    return None