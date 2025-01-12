import time
import json
from binance.um_futures import UMFutures
import numpy as np
from db import Database
from my_binance import *
import telebot

channel_id = "-1001702093331"  # The channel ID starts with a - and is followed by the channel's unique ID
bot = telebot.bot = telebot.TeleBot(token="5202575933:AAF-q7yxh_EyQBqsYtiuIViIFUHh27SFY0A")
db = Database('database .db')
def point_calculation(balance, procent, price):
    enter_usdt = float(balance) * procent / 100
    result = round(enter_usdt  * 30 / price, 3)
    return result


def get_border(interval):
    # Initialize the Binance client
    client = UMFutures()
    symbol = 'BTCUSDT'

    # Fetch historical data
    ohlcv = client.klines("BTCUSDT", interval, limit=500)

    closes = [float(x[4]) for x in ohlcv]

    # Calculate upper and lower channel boundaries
    sma = np.mean(closes, dtype=float)
    std = np.std(closes, dtype=float)
    upper = sma + 2 * std
    lower = sma - 2 * std

    ticker = client.ticker_price(symbol)
    last_price = float(ticker['price'])

    return float(upper), float(lower), last_price, interval

def enter_position(border, user_id):
    interval = border[3]
    if interval == '1m':
        procent = 20
        position = 'position_1m'
    elif interval == '5m':
        procent = 20
        position = 'position_5m'
    elif interval == '15m':
        procent = 30
        position = 'position_15m'
    elif interval == '30m':
        procent = 40
        position = 'position_30m'
    elif interval == '1h':
        procent = 60
        position = 'position_1h'
    elif interval == '4h':
        procent = 70
        position = 'position_4h'
    profit_pricent = (border[0] / border[1] * 100) - 100
    if border[2] > border[0] and db.get_position(user_id,  position) != 'SHORT': #вход позиция short
        if db.get_profit_2(user_id) == 'ON':

            if profit_pricent >= 2:
                key = db.get_api_key(user_id)
                secret = db.get_secret_key(user_id)
                db.set_position(user_id, position, 'SHORT')
                balance = balance_binance(key, secret)[0]
                qwot = point_calculation(balance, procent, border[2])
                open_order(key, secret, qwot, 'SELL', 'MARKET')
                histori = histori_traid(key, secret)[-1]
                bot.send_message(chat_id=user_id,
                                 text=f'SHORT: {interval}interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')
                if user_id == 871610428:
                    bot.send_message(chat_id=channel_id,
                                     text=f'SHORT: {interval}interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')
        else:
            key = db.get_api_key(user_id)
            secret = db.get_secret_key(user_id)
            db.set_position(user_id, position, 'SHORT')
            balance = balance_binance(key, secret)[0]
            qwot = point_calculation( balance, procent, border[2])
            open_order(key, secret, qwot, 'SELL', 'MARKET')
            histori = histori_traid(key, secret)[-1]
            bot.send_message(chat_id=user_id,
                             text=f'SHORT: {interval}interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')
            if user_id == 871610428:
                bot.send_message(chat_id=channel_id,
                                 text=f'SHORT: {interval}interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')

    elif border[2] < border[1] and db.get_position(user_id,  position) != 'LONG': # вход позиция Long
        if db.get_profit_2(user_id) == 'ON':

            if profit_pricent >= 2:
                db.set_position(user_id, position, 'LONG')
                key = db.get_api_key(user_id)
                secret = db.get_secret_key(user_id)
                balance = balance_binance(key, secret)[0]
                qwot = point_calculation(balance, procent, border[2])
                open_order(key, secret, qwot, 'BUY', 'MARKET')
                histori = histori_traid(key, secret)[-1]
                bot.send_message(chat_id=user_id,
                                 text=f'LONG: {interval}-interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')
                if user_id == 871610428:
                    bot.send_message(chat_id=channel_id,
                                     text=f'LONG: {interval}-interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')

        else:

            db.set_position(user_id, position, 'LONG')
            key = db.get_api_key(user_id)
            secret = db.get_secret_key(user_id)
            balance = balance_binance(key, secret)[0]
            qwot = point_calculation(balance, procent, border[2])
            open_order(key, secret, qwot, 'BUY', 'MARKET')
            histori = histori_traid(key, secret)[-1]
            bot.send_message(chat_id=user_id,
                             text=f'LONG: {interval}-interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')
            if user_id == 871610428:
                bot.send_message(chat_id=channel_id,
                                 text=f'LONG: {interval}-interval\n{histori["qty"]}:BTC\n{histori["price"]}:Price\n{histori["commission"]}:commission\nBalance-{balance}')


def main():

    border_1m = get_border('1m')
    border_5m = get_border('5m')
    border_15m = get_border('15m')
    border_30m = get_border('30m')
    border_1h = get_border('1h')
    border_4h = get_border('4h')
    print(f'1m: {border_1m}\n5m: {border_5m}\n15m: {border_15m}\n30m: {border_30m}\n1h: {border_1h}\n4h: {border_4h}\n')

    with open('data.txt') as json_file:
        data = json.load(json_file)
        alluser_id = data['user_id']

    for user_id in alluser_id :
        enter_position(border_1m, user_id)
        enter_position(border_5m, user_id)
        enter_position(border_15m, user_id)
        enter_position(border_30m, user_id)
        enter_position(border_1h, user_id)
        enter_position(border_4h, user_id)

    time.sleep(3)



if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            pass