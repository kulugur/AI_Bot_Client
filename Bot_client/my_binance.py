
#https://github.com/binance/binance-futures-connector-python/tree/main/examples/um_futures/trade
#!/usr/bin/env python
import logging
from binance.um_futures import UMFutures
from binance.spot import Spot as Client
from config import *
from binance.error import ClientError
import csv

key = 'CCW3X4P0vvL3PWpQdN0ZUiivCSTvEuU6Xl6m5UkCHP75oxc0bHKyN9viNnQhzH0M'
secret = 'EnWsq6BhNIUagMUA5PmmAa1Ea3r2WfB8VhZCwIzmEx6O8MmASwOpRbvOOd02g4S3'
#url = 'https://fapi.binance.com'

# key ='b4945dd41bdef055f2864eaf3488c28b3846be8c65a120b674928f62672ed48a'
# secret = 'a2acdb85925314acf6c77b5c5a741497313545d71cfeab8cd001bad018a051bb'
# url = 'https://testnet.binancefuture.com'

def read_csv(user_id):
    balance = balance_binance(key, secret)[0]
    orders = histori_traid(key, secret)[-1]
    if float(orders['realizedPnl']) > 0:
        commission_bot = round((float(orders['realizedPnl']) * 15) / 100, 3)
        deposit = float(db.get_deposit_demo(user_id)) - commission_bot
        db.set_deposit_demo(user_id, deposit)
    else:
        commission_bot = 0
    try:

        with open(f'user_csv/{user_id}.csv', 'r', newline='') as f:
            pass
        with open(f'user_csv/{user_id}.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                               orders['side'], orders['realizedPnl'], balance, commission_bot,
                               db.get_deposit_demo(user_id)])
    except:
        with open(f'user_csv/{user_id}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['date', 'Pars', 'Entry Price', 'Size        ', 'Side        ', 'Profit', 'Balance', 'Commission Bot',
                 'Balance bot'])
            writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                             orders['side'], orders['realizedPnl'], balance, commission_bot,
                             db.get_deposit_demo(user_id)])
    return True

def get_status_aip(key, secret):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.api_trading_status(recvWindow=6000)
        print(response)
        for i in response:
            print(i)
        logging.info(response)
    except ClientError as error:
        print(error.args[2])

def balance_binance(key, secret):


    um_futures_client = UMFutures(key=key, secret=secret)

    try:

        response = um_futures_client.balance(recvWindow=6000)
        for i in response:
            if i['asset'] == 'USDT':
                return i['balance'], i['asset']

    except ClientError as error:
        return error.args[2]




def get_orders(key, secret):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_orders(symbol="BTCUSDT", recvWindow=2000)
        return response

    except ClientError as error:
        return error.args[2]


def histori_traid(key, secret):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_account_trades(symbol="BTCUSDT", recvWindow=6000)
        return response
        # for i in response:
        #     print(i)
        logging.info(response)
    except ClientError as error:
        return error.args[2]

def pay_transaction(api_key, api_secret, pay_id):
    client = Client(api_key, api_secret)

    try:
        response = client.pay_history(startTimestamp=1637186702000, limit=50)
        for i in response['data']:
            if i['counterpartyId'] == int(pay_id):
                if float(i['amount']) > 0:
                    return i['orderId'], i['amount'], i['currency']
            else:
                return 'NoPay', '0', 'USDT'



    except ClientError as error:
        print(error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        ))

def get_position(key, secret):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_position_risk(symbol="BTCUSDT", recvWindow=6000)
        return response[0]['symbol'], response[0]['entryPrice'], response[0]['positionAmt'], response[0]['unRealizedProfit'], response[0]['liquidationPrice'],response[0]['markPrice']


    except ClientError as error:
         return error.args[2]
def close_order(key, secret):

    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.cancel_order(
            symbol="BTCUSDT", orderId=123456, recvWindow=2000
        )
        return response
        # for i in response:
        #     print(i)

    except ClientError as error:
        return error.args[2]

def open_order(key, secret, quantity, side, types):

    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.new_order(
            symbol="BTCUSDT",
            side=side,
            type=types,
            quantity=quantity,


        )
        return response
    except ClientError as error:
        return error.args[2]

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
def get_open_order(key, secret, orderId):
    um_futures_client = UMFutures(key=key, secret=secret)

    try:
        response = um_futures_client.get_open_orders(
            symbol="BTCUSDT", orderId=orderId, recvWindow=2000
        )
        return response
    except ClientError as error:
        return error.args[2]
#print(balance_binance(key, secret))
#print(open_order(key, secret, 0.1, 25750, 'BUY', 'TAKE_PROFIT_MARKET'))
#print(open_order_take(key, secret,  0.001, 'BUY', 'STOP_MARKET',25750))
#print(balance_binance(key, secret))
# if type(open_order(key, secret, 0.001,  'BUE', 'MARKET')) is str:
#     print('da')
#open_order(key, secret, 22350.8, 0.001,  'BUY', 'STOP')
#close_order(key, secret)
#print(histori_traid(key, secret)[-1]) #История
#print(get_orders(key, secret)) # все открытые ордера
#print(get_position(key, secret)) # открытые позиции
#print(get_status_aip(key, secret)) # статус апи
#print(pay_transaction(key, secret, 499682466))