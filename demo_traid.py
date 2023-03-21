import time
import json
from binance.um_futures import UMFutures
import numpy as np
from db import Database
from my_binance import *
import telebot

channel_id = "-1001702093331"  # The channel ID starts with a - and is followed by the channel's unique ID
bot = telebot.bot = telebot.TeleBot(token="5202575933:AAF-q7yxh_EyQBqsYtiuIViIFUHh27SFY0A")
db = Database('database.db')

def get_all_position(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            minim= 10000000
            maxim= 0
            position = 0
            if str(user_id) == i['user_id']:
                for pos in i:
                    if pos == 'user_id':
                        pass
                    elif i[pos] == '':
                        pass
                    elif pos == 'close':
                        pass
                    else:
                        if i[pos][0] > maxim:
                            maxim = i[pos][0]
                        elif i[pos][0] < minim:
                            minim = i[pos][0]
                        position += i[pos][1]
                if minim == 10000000:
                        minim = maxim
                elif maxim == 0:
                        maxim = minim
                return   position,  minim, maxim

def set_position_js(user_id, position, enter ):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                i[position] = enter

    with open('data2.txt', 'w') as outfile:

        json.dump(data, outfile)


def get_position_js(user_id, position ):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                return i[position]

def point_calculation(balance, procent, price):
    enter_usdt = float(balance) * procent / 100
    result = round(enter_usdt * 4 / price, 3)

    return result, enter_usdt
def close_position(user_id, price):
    balance = db.get_deposit_demo(user_id)
    position = db.get_position_balance(user_id)
    enter_price = get_all_position(user_id)
    if enter_price == None:
        db.set_position_balance(user_id, 0)
        return
    elif enter_price[0] == 0:
        db.set_position_balance(user_id, 0)
        return
    elif position > 0:
        balance += ((price - enter_price[1]) * position) / 4
    else:
        balance += ((price - enter_price[2]) * position) / 4
    db.set_deposit_demo(user_id, balance)
    db.set_position_balance(user_id, 0)



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
        procent = 10
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
        procent = 50
        position = 'position_1h'
    elif interval == '4h':
        procent = 60
        position = 'position_4h'
    profit_pricent = (border[0] / border[1] * 100) - 100
    if border[2] >= border[0] and db.get_position(user_id,  position) != 'SHORT': #вход позиция short
        if db.get_profit_2(user_id) == 'ON':

            if profit_pricent >= 2:
                db.set_position(user_id, position, 'SHORT')
                balance = db.get_deposit_demo(user_id)

                qwot = point_calculation(balance, procent, border[2])
                position_balance = db.get_position_balance(user_id)
                res_pos = position_balance - qwot[0]
                db.set_position_balance(user_id, res_pos)
                old_position = get_position_js(user_id, position)
                if old_position != '':
                    set_position_js(user_id, position, '')
                    bot.send_message(chat_id=user_id,
                                     text=f'Profit{interval} {(border[2] - old_position[0]) * qwot[0]}')
                    balance += ((border[2] - old_position[0]) * qwot[0]) + qwot[1] / 4
                else:
                    set_position_js(user_id, position, [border[2], res_pos])
                    balance -= qwot[1] / 4
                db.set_deposit_demo(user_id, balance)

                bot.send_message(chat_id=user_id,
                                 text=f'SHORT: {interval} interval\n{qwot[0]}:BTC\n{border[2]}:Price\nBalance: {db.get_deposit_demo(user_id)}\nPosition:{db.get_position_balance(user_id)}')
                db.set_position(user_id, position, 'SHORT')

        else:
            db.set_position(user_id, position, 'SHORT')
            balance = db.get_deposit_demo(user_id)

            qwot = point_calculation(balance, procent, border[2])
            position_balance = db.get_position_balance(user_id)
            res_pos = position_balance - qwot[0]
            db.set_position_balance(user_id, res_pos)
            old_position = get_position_js(user_id, position)
            if old_position != '':
                set_position_js(user_id, position, '')
                bot.send_message(chat_id=user_id,text=f'Profit{interval} {(border[2] - old_position[0]) * qwot[0]}')
                balance += ((border[2] - old_position[0]) * qwot[0]) + qwot[1]/4
            else:
                set_position_js(user_id, position, [border[2],res_pos])
                balance -= qwot[1]/4
            db.set_deposit_demo(user_id, balance)

            bot.send_message(chat_id=user_id,
                             text=f'SHORT: {interval} interval\n{qwot[0]}:BTC\n{border[2]}:Price\nBalance: {db.get_deposit_demo(user_id)}\nPosition:{db.get_position_balance(user_id)}')
            db.set_position(user_id, position, 'SHORT')


    elif border[2] < border[1] and db.get_position(user_id,  position) != 'LONG': # вход позиция Long
        if db.get_profit_2(user_id) == 'ON':
            balance = db.get_deposit_demo(user_id)

            qwot = point_calculation(balance, procent, border[2])
            position_balance = db.get_position_balance(user_id)
            res_pos = position_balance + qwot[0]
            db.set_position_balance(user_id, res_pos)
            old_position = get_position_js(user_id, position)

            if old_position != '':
                set_position_js(user_id, position, '')
                bot.send_message(chat_id=user_id,
                                 text=f'Profit {interval} {(border[2] - old_position[0]) * (-1 * qwot[0])}')
                balance += ((border[2] - old_position[0]) * (qwot[0] * -1)) + qwot[1] / 4

            else:
                set_position_js(user_id, position, [border[2], res_pos])
                balance -= qwot[1] / 4
            db.set_deposit_demo(user_id, balance)
            bot.send_message(chat_id=user_id,
                             text=f'LONG: {interval} interval\n{qwot[0]}:BTC\n{border[2]}:Price\nBalance: {db.get_deposit_demo(user_id)}\nPosition:{db.get_position_balance(user_id)}')
            db.set_position(user_id, position, 'LONG')
        else:



            balance = db.get_deposit_demo(user_id)

            qwot = point_calculation(balance, procent, border[2])
            position_balance = db.get_position_balance(user_id)
            res_pos = position_balance + qwot[0]
            db.set_position_balance(user_id, res_pos)
            old_position = get_position_js(user_id, position)

            if old_position != '':
                set_position_js(user_id, position, '')
                bot.send_message(chat_id=user_id, text=f'Profit {interval} {(border[2] - old_position[0]) * (-1 * qwot[0])}')
                balance += ((border[2] - old_position[0]) * (qwot[0]* -1)) + qwot[1]/4

            else:
                set_position_js(user_id, position, [border[2], res_pos])
                balance -= qwot[1] / 4
            db.set_deposit_demo(user_id, balance)
            bot.send_message(chat_id=user_id,
                             text=f'LONG: {interval} interval\n{qwot[0]}:BTC\n{border[2]}:Price\nBalance: {db.get_deposit_demo(user_id)}\nPosition:{db.get_position_balance(user_id)}')
            db.set_position(user_id, position, 'LONG')

def main():

    border_1m = get_border('1m')
    border_5m = get_border('5m')
    border_15m = get_border('15m')
    border_30m = get_border('30m')
    border_1h = get_border('1h')
    border_4h = get_border('4h')
    print(f'1m: {border_1m}\n5m: {border_5m}\n15m: {border_15m}\n30m: {border_30m}\n1h: {border_1h}\n4h: {border_4h}\n')

    with open('data2.txt') as json_file:
        data = json.load(json_file)


    for user_id in data :
        enter_position(border_1m, user_id['user_id'])
        enter_position(border_5m, user_id['user_id'])
        enter_position(border_15m, user_id['user_id'])
        enter_position(border_30m, user_id['user_id'])
        enter_position(border_1h, user_id['user_id'])
        enter_position(border_4h, user_id['user_id'])

    time.sleep(3)



if __name__ == '__main__':
    while True:
        main()


