import time
import json
import numpy as np
from hendlers_fun import position, my_balance
from my_binance import *
import telebot
from config import *
import asyncio

print('Start_v2.0')

bot = telebot.bot = telebot.TeleBot(token=TOKEN)
channel_id = "-1001702093331"
db = Database('database.db')


def point_calculation(balance, procent, price):
    enter_usdt = float(balance) * procent / 100
    result = round(enter_usdt / price, 3)
    if result < 0.001:
        result = 0.001
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

    return float(upper), float(lower), last_price


def message_all_users(text):  # отправка сообшения всем пользователям
    with open('data2.txt') as json_file:
        data2 = json.load(json_file)
    for user_id in data2:
        try:

            bot.send_message(chat_id=user_id['user_id'],
                             text=text)
        except:
            print(user_id['user_id'])


async def enter_position(user_id):
    interval = ['1m', '5m', '15m', '30m', '1h', '4h']
    for i in interval:
        border = get_border(i)
        if i == '1m':
            procent = 5
            position_interval = 'position_1m'
        elif i == '5m':
            procent = 10
            position_interval = 'position_5m'
        elif i == '15m':
            procent = 15
            position_interval = 'position_15m'
        elif i == '30m':
            procent = 20
            position_interval = 'position_30m'
        elif i == '1h':
            procent = 25
            position_interval = 'position_1h'
        elif i == '4h':
            procent = 30
            position_interval = 'position_4h'
        if user_id == tg_chanel_user:
            url = 'https://testnet.binancefuture.com'
        else:
            url = 'https://fapi.binance.com'

        profit_pricent = (border[0] / border[1] * 100) - 100

        if border[2] > border[0] and db.get_position(user_id, position_interval) != 'SHORT':  # вход позиция short
            if db.get_profit_2(user_id) == 'ON':
                if profit_pricent >= 2:
                    await my_balance(user_id)
                    await enter_binance(user_id, url, procent, border, position_interval, 'SHORT')
            else:
                await my_balance(user_id)
                await enter_binance(user_id, url, procent, border, position_interval, 'SHORT')

        elif border[2] < border[1] and db.get_position(user_id, position_interval) != 'LONG':  # вход позиция Long
            if db.get_profit_2(user_id) == 'ON':
                if profit_pricent >= 2:
                    await my_balance(user_id)
                    await enter_binance(user_id, url, procent, border, position_interval, 'LONG')
            else:
                await my_balance(user_id)
                await enter_binance(user_id, url, procent, border, position_interval, 'LONG')


async def enter_binance(user_id, url, procent, border, position_interval, position):  # вход по рынку Binance
    try:
        if position == 'SHORT':
            size = 'SELL'
        else:
            size = 'BUY'
        key = db.get_api_key(user_id)
        secret = db.get_secret_key(user_id)
        position_my = get_position(key, secret, url)
        balance = balance_binance(key, secret, url)[0]
        qwot = point_calculation(balance, procent, border[2])
        res = open_order(key, secret, qwot, size, 'MARKET', url)
        db.set_position(user_id, position_interval, position)
        if type(res) is str:
            bot.send_message(chat_id=user_id, text=f'{position}: {qwot}\nERROR: {res}')
        else:
            await asyncio.sleep(5)
            orders = histori_traid(key, secret, url)[-1]

            bot.send_message(chat_id=user_id,
                             text=f'{position}:\nBTC: {orders["qty"]}\nPrice: {orders["price"]}\nCommission: {orders["commission"]}\nBalance: {balance}\n\n{position_my[0]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')
            if user_id == tg_chanel_user:
                message_all_users(
                    f'{position}:\nBTC: {orders["qty"]}\nPrice: {orders["price"]}\nCommission: {orders["commission"]}\nBalance: {balance}\n\n{position_my[0]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')
    except:
        bot.send_message(chat_id=user_id, text=f'{position}: {qwot}\nERROR:')
        return 'error'


async def main():
    while True:
        try:
            with open('data.txt') as json_file:
                data = json.load(json_file)
                alluser_id = data['user_id']

            for user_id in alluser_id:
                task = asyncio.create_task(enter_position(user_id))
            await task
            time.sleep(3)
        except:
            pass


if __name__ == '__main__':
    asyncio.run(main())