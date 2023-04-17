
from config import *
from aiogram import Bot, Dispatcher


import markups as nav
from db import Database

from my_binance import balance_binance, get_position
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


admin = [871610428]

async def position(from_user):
    subscription = db.get_subscription(from_user)
    if subscription == 'Light':
        url = 'https://testnet.binancefuture.com'
        id_key = admin[0]
    else:
        url = 'https://fapi.binance.com'
        id_key = from_user
    key = db.get_api_key(id_key)
    secret = db.get_secret_key(id_key)
    if key != None or secret != None:
        try:
            position_my = get_position(key, secret, url)
        except:
            await bot.send_message(from_user, 'Binance API Error', reply_markup=nav.eng_registr)
        if type(position_my) is str:
            await bot.send_message(from_user, text=f'ERROR: API-KEY Futures', reply_markup=nav.eng_registr)
        else:
            await bot.send_message(from_user,
                                   f'{position_my[0]}\nMarketPrice: {position_my[5]}\nEntry Price: {position_my[1]}\nSize: {position_my[2]}\nPNL: {position_my[3]}')
    else:
        await bot.send_message(from_user, 'No Binance API', reply_markup=nav.eng_registr)

async def my_balance(from_user):
    subscription = db.get_subscription(from_user)
    if subscription == 'Light':
        url = 'https://testnet.binancefuture.com'
        id_key = admin[0]
    else:
        url = 'https://fapi.binance.com'
        id_key = from_user
    key = db.get_api_key(id_key)
    secret = db.get_secret_key(id_key)
    if key != None or secret != None:
        try:
            balance = balance_binance(key, secret, url)
        except:
            await bot.send_message(from_user, 'Binance API Error', reply_markup=nav.eng_registr)
        if type(balance) is str:
            await bot.send_message(from_user, text=f'ERROR: API-KEY Futures',
                                   reply_markup=nav.eng_registr)
        else:
            await bot.send_message(from_user, f'Balance USDT: {balance[0]}')
    else:
        await bot.send_message(from_user, 'No Binance API', reply_markup=nav.eng_registr)