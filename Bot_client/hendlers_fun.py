import asyncio
import csv
from config import *
from aiogram import Bot, Dispatcher
from my_binance import *

import markups as nav
from db import Database

from my_binance import balance_binance, get_position
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


admin = [871610428]

async def position(from_user):
    subscription = db.get_subscription(from_user)
    if subscription == 'Lite':

        id_key = admin[0]
    else:

        id_key = from_user
    key = db.get_api_key(id_key)
    secret = db.get_secret_key(id_key)
    if key != None or secret != None:
        try:
            position_my = get_position(key, secret)
        except:
            await bot.send_message(from_user, 'Binance API Error', reply_markup=nav.eng_registr)
        if type(position_my) is str:
            await bot.send_message(from_user, text=f'ERROR: API-KEY Futures', reply_markup=nav.eng_registr)
        else:
            if float(position_my[2]) > 0:
                tupe = 'Long'
            elif float(position_my[2]) == 0:
                tupe = 'No position'
            else:
                tupe = 'Short'
            await bot.send_message(from_user,
                                   f'{position_my[0]}\n{tupe}\nMarketPrice: {position_my[5]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')
    else:
        await bot.send_message(from_user, 'No Binance API', reply_markup=nav.eng_registr)

async def my_balance(from_user):
    subscription = db.get_subscription(from_user)
    if subscription == 'Lite':

        id_key = admin[0]
    else:

        id_key = from_user
    key = db.get_api_key(id_key)
    secret = db.get_secret_key(id_key)
    if key != None or secret != None:
        try:
            balance = balance_binance(key, secret)
        except:
            await bot.send_message(from_user, 'Binance API Error', reply_markup=nav.eng_registr)
        if type(balance) is str:
            await bot.send_message(from_user, text=f'ERROR: API-KEY Futures',
                                   reply_markup=nav.eng_registr)
        else:
            await bot.send_message(from_user, f'Balance USDT: {balance[0]}')
            db.set_binance_balance(from_user, balance[0] )
            db.set_binance_traid(from_user, 'ON')
    else:
        await bot.send_message(from_user, 'No Binance API', reply_markup=nav.eng_registr)


async def averaging(from_user):

    key = db.get_api_key(from_user)
    secret = db.get_secret_key(from_user)
    position_my = get_position(key, secret)
    if float(position_my[3]) < 0:
        if float(position_my[5]) > float(position_my[1]):
            pos = 'SELL'
        else:
            pos = 'BUY'
        size = float(position_my[2])
        open_order(key, secret, size,  pos, 'MARKET')
        return f'Position {size} {pos}'
    return 'None Position'

async def buy(user_id):

    key = db.get_api_key(user_id)
    secret = db.get_secret_key(user_id)
    size = 0.005
    balance = balance_binance(key, secret)[0]
    position_my = get_position(key, secret)
    open_order(key, secret, size,  'BUY', 'MARKET')
    await asyncio.sleep(5)
    orders = histori_traid(key, secret)[-1]
    try:
        if float(orders['realizedPnl']) > 0:
            commission_bot = float(orders['realizedPnl']) * 15 / 100
            commission_bot = round(commission_bot, 3)
            deposit = float(db.get_deposit_demo(user_id)) - commission_bot
            db.set_deposit_demo(user_id, deposit)
            print(f"{commission_bot} commission_bot")
        else:
            commission_bot = 0
    except Exception as e:
        await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\ncommission_bot ')
    try:
        try:

            with open(f'user_csv/{user_id}.csv', 'r', newline='') as f:
                pass
            with open(f'user_csv/{user_id}.csv', 'a', newline='') as f:
                try:
                    writer = csv.writer(f)
                    writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                                     orders['side'], orders['realizedPnl'], balance, commission_bot,
                                     db.get_deposit_demo(user_id)])
                except Exception as e:
                    await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\nread user_csv')
                    await bot.send_message(chat_id=871610428, text=f'{user_id}\n{orders}\nread user_csv')
        except:
            with open(f'user_csv/{user_id}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['date', 'Pars', 'Entry Price', 'Size        ', 'Side        ', 'Profit', 'Balance',
                     'Commission Bot',
                     'Balance bot'])
                writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                                 orders['side'], orders['realizedPnl'], balance, commission_bot,
                                 db.get_deposit_demo(user_id)])
    except Exception as e:
        await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\nread user_csv')
    await bot.send_message(chat_id=user_id,
                     text=f'{position}:\nBTC: {orders["qty"]}\nPrice: {orders["price"]}\nCommission: {orders["commission"]}\nBalance: {balance}\n\n{position_my[0]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')


async def sell(user_id):

    key = db.get_api_key(user_id)
    secret = db.get_secret_key(user_id)
    size = 0.005
    balance = balance_binance(key, secret)[0]
    position_my = get_position(key, secret)
    open_order(key, secret, size,  'SELL', 'MARKET')
    await asyncio.sleep(5)
    orders = histori_traid(key, secret)[-1]
    try:
        if float(orders['realizedPnl']) > 0:
            commission_bot = float(orders['realizedPnl']) * 15 / 100
            commission_bot = round(commission_bot, 3)
            deposit = float(db.get_deposit_demo(user_id)) - commission_bot
            db.set_deposit_demo(user_id, deposit)
            print(f"{commission_bot} commission_bot")
        else:
            commission_bot = 0
    except Exception as e:
        await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\ncommission_bot ')
    try:
        try:

            with open(f'user_csv/{user_id}.csv', 'r', newline='') as f:
                pass
            with open(f'user_csv/{user_id}.csv', 'a', newline='') as f:
                try:
                    writer = csv.writer(f)
                    writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                                     orders['side'], orders['realizedPnl'], balance, commission_bot,
                                     db.get_deposit_demo(user_id)])
                except Exception as e:
                    await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\nread user_csv')
                    await bot.send_message(chat_id=871610428, text=f'{user_id}\n{orders}\nread user_csv')
        except:
            with open(f'user_csv/{user_id}.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['date', 'Pars', 'Entry Price', 'Size        ', 'Side        ', 'Profit', 'Balance',
                     'Commission Bot',
                     'Balance bot'])
                writer.writerow([orders['time'], orders['symbol'], orders['price'], orders['qty'],
                                 orders['side'], orders['realizedPnl'], balance, commission_bot,
                                 db.get_deposit_demo(user_id)])
    except Exception as e:
        await bot.send_message(chat_id=871610428, text=f'{user_id}\n{e}\nread user_csv')
    await bot.send_message(chat_id=user_id,
                           text=f'{position}:\nBTC: {orders["qty"]}\nPrice: {orders["price"]}\nCommission: {orders["commission"]}\nBalance: {balance}\n\n{position_my[0]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')

# task = asyncio.create_task(my_balance(6295959004))
# asyncio.run(my_balance(6295959004))
