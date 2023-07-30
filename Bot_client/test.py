import time
import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError


key = 'CCW3X4P0vvL3PWpQdN0ZUiivCSTvEuU6Xl6m5UkCHP75oxc0bHKyN9viNnQhzH0M'
secret = 'EnWsq6BhNIUagMUA5PmmAa1Ea3r2WfB8VhZCwIzmEx6O8MmASwOpRbvOOd02g4S3'
def open_order_take(key, secret, quantity, side, types, price):

    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.new_order(
            symbol="BTCUSDT",
            side=side,
            type=types,
            quantity=quantity,
            stopPrice=price,


        )

        return response
    except ClientError as error:
        return error.args[2]
def stop_market(key, secret, types, price):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.new_order(
            symbol="BTCUSDT",
            type=types,
            stopPrice=price,

        )

        return response
    except ClientError as error:
        return error.args[2]
def get_position(key, secret):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_position_risk(symbol="BTCUSDT", recvWindow=6000)
        return response[0]['symbol'], response[0]['entryPrice'], response[0]['positionAmt'], response[0]['unRealizedProfit'], response[0]['liquidationPrice'],response[0]['markPrice']


    except ClientError as error:
         return error.args[2]

def get_open_order(key, secret, orderId):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_open_orders(
            symbol="BTCUSDT", orderId=orderId, recvWindow=2000
        )
        return response
    except ClientError as error:
        return error.args[2]


orderid_sell = None
orderid_buy =None
while True:
    # Initialize the Binance client
    client = UMFutures()
    symbol = 'BTCUSDT'
    ohlcv = client.klines("BTCUSDT", '1m', limit=50)
    line_min = False
    line_max = False
    for i in ohlcv:

        if not line_min or float(i[4]) < line_min:
            line_min = float(i[4])
            line_procent = line_min * 0.2 / 100
            line_min_max = line_min + line_procent
            line_min_min = line_min - line_procent

        if not line_max or float(i[4]) > line_max:
            line_max = float(i[4])
            line_procent = line_max * 0.2 / 100
            line_max_max = line_max + line_procent
            line_max_min = line_max - line_procent
        #print('Open', i[1], 'Max', i[2], 'min', i[3], 'close', i[4], 'value')
    #print(line_max)
    #print(line_min)
    print('line_min', [line_min_max, line_min_min])
    print('line_max', [line_max_max, line_max_min])
    book_orders = client.depth("BTCUSDT", **{"limit": 1000})
    order_max = False
    for i in book_orders['asks']:
        if not order_max or float(i[1]) > order_max:
            order_max = float(i[1])
            order_asks = i
    order_max = False
    for i in book_orders['bids']:
        if not order_max or float(i[1]) > order_max:
            order_max = float(i[1])
            order_bids = i

    if float(order_bids[0]) < line_min_max and float(order_bids[0]) > line_min_min and float(order_bids[1]) > 100:
        # Размешяем отложенный ордер на продажу
        if orderid_sell == None:
            orderid_sell = open_order_take(key, secret, 0.001, 'SELL', 'STOP_MARKET', float(order_bids[0]))
        print(order_bids, 'sell')
    if orderid_sell != None:
            # Если ордер исполнен размешяем стоп лос в безубыток
        position = get_position(key, secret)
        if float(position[2]) != 0:
            print(position)
            open_order_take(key, secret, float(position[2]), 'BUY', 'STOP_MARKET', float(position[1]))
            orderid_sell = None

        # Если ордер исполнен размешяем стоп лос в безубыток
        # выставляем тейк профит
        # Отменяем ордер на покупку

    if float(order_asks[0]) < line_max_max and float(order_asks[0]) > line_max_min and float(order_asks[1]) > 100:
        # Размешяем отложенный ордер на пакупку
        if orderid_buy == None:
            orderid_buy = open_order_take(key, secret, 0.001, 'BUY', 'STOP_MARKET', float(order_asks[0]))
        print(order_asks, 'buy')

    if orderid_buy != None:
            # Если ордер исполнен размешяем стоп лос в безубыток
        position = get_position(key, secret)
        if float(position[2]) != 0:
            print(position)
            open_order_take(key, secret, float(position[2]), 'SELL', 'STOP_MARKET', float(position[1]))
            orderid_buy = None

    print('asks', order_asks )
    print('bids', order_bids)

    time.sleep(5)

