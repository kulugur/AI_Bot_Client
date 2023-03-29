
#https://github.com/binance/binance-futures-connector-python/tree/main/examples/um_futures/trade
#!/usr/bin/env python
import logging
from binance.um_futures import  UMFutures

from binance.error import ClientError

# key ='GyvAV7Mqrcww6jsmKkJaaF6INUgMbluM4ydxyiFHE3ioOE87Seym1xJWW3u98AHR'
# secret= 'VOmu6fEU4ecqMQOJvXmwAzx64E8yOmpmuQDdtjatV2yoxZbzznLFHNs9hRtnakbV'

key ='b4945dd41bdef055f2864eaf3488c28b3846be8c65a120b674928f62672ed48a'
secret = 'a2acdb85925314acf6c77b5c5a741497313545d71cfeab8cd001bad018a051bb'
url = 'https://testnet.binancefuture.com'

def get_status_aip(key, secret, url):
    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:
        response = um_futures_client.api_trading_status(recvWindow=6000)
        print(response)
        for i in response:
            print(i)
        logging.info(response)
    except ClientError as error:
        print(error.args[2])

def balance_binance(key, secret, url):


    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:

        response = um_futures_client.balance(recvWindow=6000)
        for i in response:
            if i['asset'] == 'USDT':
                return i['balance'], i['asset']

    except ClientError as error:
        return error.args[2]




def get_orders(key, secret, url):
    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:
        response = um_futures_client.get_orders(symbol="BTCUSDT", recvWindow=2000)
        return response

    except ClientError as error:
        return error.args[2]


def histori_traid(key, secret, url):
    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:
        response = um_futures_client.get_account_trades(symbol="BTCUSDT", recvWindow=6000)
        return response
        # for i in response:
        #     print(i)
        logging.info(response)
    except ClientError as error:
        return error.args[2]

def get_position(key, secret, url):
    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:
        response =  um_futures_client.get_position_risk(symbol="BTCUSDT", recvWindow=6000)
        return response[0]['symbol'], response[0]['entryPrice'], response[0]['positionAmt'], response[0]['unRealizedProfit'], response[0]['liquidationPrice']


    except ClientError as error:
        return error.args[2]
def close_order(key, secret, url):

    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

    try:
        response = um_futures_client.cancel_order(
            symbol="BTCUSDT", orderId=123456, recvWindow=2000
        )
        return response
        # for i in response:
        #     print(i)

    except ClientError as error:
        return error.args[2]

def open_order(key, secret, quantity, side, types, url):

    um_futures_client = UMFutures(key=key, secret=secret, base_url=url)

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


#print(balance_binance(key, secret, url))
#print(open_order(key, secret, 0.1,  'BUY', 'MARKET', url))
# if type(open_order(key, secret, 0.001,  'BUE', 'MARKET')) is str:
#     print('da')
#open_order(key, secret, 22350.8, 0.001,  'BUY', 'STOP')
#close_order(key, secret, url)
#print(histori_traid(key, secret, url)[-1]) #История
#print(get_orders(key, secret, url)) # все открытые ордера
#print(get_position(key, secret, url)) # открытые позиции
#print(get_status_aip(key, secret, url)) # статус апи