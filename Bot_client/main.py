import logging
import json
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

import markups as nav
from db import Database
from binance.um_futures import UMFutures
from my_binance import balance_binance

from binance.error import ClientError
tg_chanel_user = 871610428
admin = [871610428]

users = [871610428, 634713845, -1001877258339]

def set_user_js(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        user =[]
        for i in data:

            user.append(i['user_id'])

        if str(user_id) in user:
            print('такой юзер уже есть')

        else:
            data.append({
            'user_id':str(user_id),
            'position_1m':'',
            'position_5m':'',
            'position_15m':'',
            'position_30m':'',
            'position_1h':'',
            'position_4h':'',
            'close':'',

            })
        with open('data2.txt', 'w') as outfile:

            json.dump(data, outfile)

def set_position_js(user_id, position, enter ):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                i[position] = enter

    with open('data2.txt', 'w') as outfile:

        json.dump(data, outfile)

def del_user_js(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                data.pop(data.index(i))
    with open('data2.txt', 'w') as outfile:

        json.dump(data, outfile)




TOKEN = '5202575933:AAF-q7yxh_EyQBqsYtiuIViIFUHh27SFY0A'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')

@dp.message_handler(commands=['rus'])
async def start(message: types.Message):
    db.set_language(message.from_user.id, 'ru')
    await bot.send_message(message.from_user.id, 'Язык изменён на Русский\nНажми /start')

@dp.message_handler(commands=['eng'])
async def start(message: types.Message):
    db.set_language(message.from_user.id, 'eng')
    await bot.send_message(message.from_user.id, 'Language changed to English\nClick /start')
@dp.message_handler(lambda message: message.chat.id in admin, commands=['admin'])
async def start(message: types.Message):
    all_user = db.get_all()
    text = ''
    for i in all_user:
        text +=f'id {i[1]} НИК {i[2]} Подписка{i[5]} leng {i[14]} balance {i[23]}\n\n'

    await bot.send_message(message.from_user.id, text)



@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await bot.send_message(871610428, f'новый пользовател {message.from_user.id}')
        if message.from_user.locale.language == 'ru':
            db.set_language(message.from_user.id, 'ru')
            await bot.send_message(message.from_user.id, 'Ваш язык определён как Русский изменить можно в дополнительных настройках')


        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Enter your nickname:')
        else:
            await bot.send_message(message.from_user.id, 'Укажите ваш ник:')
    else:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Main menu!', reply_markup=nav.eng_mainMenu)
        else:
            await bot.send_message(message.from_user.id, 'Главное меню!', reply_markup=nav.mainMenu)

@dp.message_handler()
async def bot_masege(message: types.Message):
    if message.chat.type == 'private':
        if message.text == '👽 Профиль' or  message.text == '👽 Profile':
            await bot.send_message(message.from_user.id, '👽️')
            if db.get_api_key(message.from_user.id) != None and db.get_secret_key(message.from_user.id) != None:
                binance_api = 'Yes'
            else:
                binance_api = 'No'
            nicname = db.get_nickname(message.from_user.id)
            timeSub = db.get_time_sub(message.from_user.id)
            subscription = db.get_subscription(message.from_user.id)
            wallet = db.get_wallet(message.from_user.id)

            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nNickname: {nicname}\nWallet {wallet}\nYour subscription: {subscription}\nBinance_api: {binance_api}\nLeft: {timeSub} days')

            else:
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nНик: {nicname}\nКошелек {wallet}\nВаша подписка: {subscription}\nBinance_api: {binance_api}\nОсталось: {timeSub} дней')

        elif message.text == '👣Назад' or message.text == '👣Back':
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,'👣', reply_markup=nav.eng_mainMenu)


            else:
                await bot.send_message(message.from_user.id,'👣', reply_markup=nav.mainMenu)


        elif message.text == 'ℹ️Инфо' or  message.text == 'ℹ️Info':
            await bot.send_message(message.from_user.id, 'ℹ️')
            nicname = db.get_nickname(message.from_user.id)
            timeSub = db.get_time_sub(message.from_user.id)
            subscription = db.get_subscription(message.from_user.id)
            wallet = db.get_wallet(message.from_user.id)
            if db.get_api_key(message.from_user.id) != None and db.get_secret_key(message.from_user.id) != None:
                binance_api = 'Yes'
            else:
                binance_api = 'No'
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nNickname: {nicname}\nWallet: {wallet}\nBinance_api: {binance_api}\nYour subscription: {subscription}\nLeft: {timeSub} days\nMain group:https://t.me/ai_binance_trading\nDevelopment support: https://t.me/+VWFxrDjnK59kMTM6')

            else:
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nНик: {nicname}\nКошелек: {wallet}\nBinance_api: {binance_api}\nВаша подписка: {subscription}\nОсталось: {timeSub} дней\nГлавная группа:https://t.me/ai_binance_trading\nРазработка поддержка: https://t.me/ai_trade_rus')

        elif message.text == '✍️Подписка' or  message.text == '✍️Subscribe':
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,'✍')
                await bot.send_message(message.from_user.id, f'Your subscription: {db.get_subscription(message.from_user.id)}', reply_markup=nav.puyMenu)

            else:
                await bot.send_message(message.from_user.id, '✍')
                await bot.send_message(message.from_user.id, f'Ваша подписка: {db.get_subscription(message.from_user.id)}', reply_markup=nav.puyMenu)

            # await bot.send_message(message.from_user.id, '✍')
            # await bot.send_message(message.from_user.id,  '*****************************', reply_markup=nav.sub_inlain_Tester)
            # await bot.send_message(message.from_user.id, 'Подписка для тестировщика\nдоступны все функции\nс подключением кошелька')
            # await bot.send_message(message.from_user.id, '*****************************', reply_markup=nav.sub_inlain_Light)
            # await bot.send_message(message.from_user.id, 'Подписка Лайт\nдоступны базовые настройки\nбез подключения кошелька')
            # await bot.send_message(message.from_user.id, '*****************************', reply_markup=nav.sub_inlain_Optimum)
            # await bot.send_message(message.from_user.id, 'Подписка Optima\nдоступны базовые настройки\nс подключением кошелька')
            # await bot.send_message(message.from_user.id, '*****************************', reply_markup=nav.sub_inlain_Premium)
            # await bot.send_message(message.from_user.id, 'Подписка Премиум\nдоступны все функции\nс подключением кошелька')
        elif message.text == '📈️Торговля' or  message.text == '📈️Trading':
            await bot.send_message(message.from_user.id, '📈️')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, f'Your subscription {db.get_subscription(message.from_user.id)}\nTo exit to the Main Menu, enter\n/start', reply_markup=nav.eng_tradingMenu)

            else:
                await bot.send_message(message.from_user.id, f'Ваша подписка {db.get_subscription(message.from_user.id)}\nДля возврата нажмите /start', reply_markup=nav.tradingMenu)

        elif message.text == '⚙️Настройки' or  message.text == '⚙️Settings':
            await bot.send_message(message.from_user.id, '⚙️')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '⚙️Settings', reply_markup=nav.eng_puyRegWallet)
            else:
                await bot.send_message(message.from_user.id, '⚙️Настройки', reply_markup=nav.puyRegWallet)

        elif message.text == '📝Регистрация' or  message.text == '📝Registration':
            await bot.send_message(message.from_user.id, '📝')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '📝Registration', reply_markup=nav.eng_registr)

            else:
                await bot.send_message(message.from_user.id, '📝Регистрация,', reply_markup=nav.eng_registr)

            #     await bot.send_message(message.from_user.id, 'Enter wallet USDT Tron (TRC20) ',
            #                            reply_markup=nav.eng_mainMenu)
            # else:
            #     await bot.send_message(message.from_user.id, 'Введите кошелек USDT Tron (TRC20) ',
            #                            reply_markup=nav.mainMenu)



        elif message.text == '⚙️Дополнительные команды' or  message.text == '⚙️Additional commands':
            await bot.send_message(message.from_user.id, 'English language /eng\nRussian language /rus\nMain Menu /start')


        elif message.text == '🤖Параметры' or  message.text == '🤖Options':
            await bot.send_message(message.from_user.id, '🤖')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '*                  RSI                 *',
                                       reply_markup=nav.settingRSI)
            else:
                await bot.send_message(message.from_user.id, '*                  RSI                 *',
                                       reply_markup=nav.settingRSI)


            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, 'Minimum profit 2%', reply_markup=nav.settingProfit)
            else:
                await bot.send_message(message.from_user.id, 'Минимальный профит 2%', reply_markup=nav.settingProfit)
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '*         Averaging          *',
                                       reply_markup=nav.settingAveraging)
            else:
                await bot.send_message(message.from_user.id, '*         Усреднение          *', reply_markup=nav.settingAveraging)
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '*Connection Binance *', reply_markup=nav.settingbinance_traid)
            else:
                await bot.send_message(message.from_user.id, '*Подключить Binance *', reply_markup=nav.settingbinance_traid)




        elif message.text == '🏁️Запустить' or  message.text == '🏁️Start':
            await bot.send_message(message.from_user.id, '🏁️')
            if not db.get_start(message.from_user.id):
                if db.get_subscription(message.from_user.id) != 'Light':
                    try:
                        if message.from_user.id == tg_chanel_user:
                            url = 'https://testnet.binancefuture.com'
                        else:
                            url = 'https://api.binance.com'
                        test = balance_binance(db.get_api_key(message.from_user.id), db.get_secret_key(message.from_user.id), url)
                    except:
                        test = 'error'
                    if test == 'error':
                        if db.get_language(message.from_user.id) == 'eng':

                            await bot.send_message(message.from_user.id,
                                                   f'Error connecting to Binance')
                        else:
                            await bot.send_message(message.from_user.id,f'Ошибка подключения к binance')
                    else:
                        db.set_binance_balance(message.from_user.id, test[0])
                        if db.get_language(message.from_user.id) == 'eng':

                            await bot.send_message(message.from_user.id, f'The trading bot is running!\nParameters:\nRSI: {db.get_rsi(message.from_user.id)}\nmin profit 2%: {db.get_profit_2(message.from_user.id)}\nAveraging: {db.get_averaging(message.from_user.id)}\nConnection Binance: {db.get_binance_traid(message.from_user.id)}\nExchange balance: {balance_binance(db.get_api_key(message.from_user.id), db.get_secret_key(message.from_user.id), url)}')
                        else:
                            await bot.send_message(message.from_user.id, f'Торговый бот запущен!\nПараметры:\nRSI: {db.get_rsi(message.from_user.id)}\nmin profit 2%: {db.get_profit_2(message.from_user.id)}\nAveraging: {db.get_averaging(message.from_user.id)}\nConnection Binance: {db.get_binance_traid(message.from_user.id)}\nБаланс биржы: {balance_binance(db.get_api_key(message.from_user.id), db.get_secret_key(message.from_user.id), url)}')
                        db.set_start(message.from_user.id, True)
                        with open('data.txt') as json_file:
                            data = json.load(json_file)
                            data['user_id'].append(message.from_user.id)

                        with open('data.txt', 'w') as outfile:
                            json.dump(data, outfile)

                else:
                    #db.set_position_balance(message.from_user.id, 0.00000001)
                    set_user_js(message.from_user.id)

                    db.set_start(message.from_user.id, True)
                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, f'Open position: {round(db.get_position_balance(message.from_user.id),3)}BTC\nBalance: {round(db.get_deposit_demo(message.from_user.id),3)} ')
                    else:
                        await bot.send_message(message.from_user.id, f'Открытая позиция: {round(db.get_position_balance(message.from_user.id),3)}BTC\n Balance: {round(db.get_deposit_demo(message.from_user.id),3)}')

            else:
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'The trading bot is already running! ')
                else:
                    await bot.send_message(message.from_user.id, 'Торговый бот уже запущен! ')

        elif message.text == '🛑Остановить' or  message.text == '🛑Stop':
            await bot.send_message(message.from_user.id, '🛑')
            if db.get_start(message.from_user.id):
                if db.get_subscription(message.from_user.id) != 'Light':
                    db.set_start(message.from_user.id, False)

                    with open('data.txt') as json_file:
                        data = json.load(json_file)
                        data['user_id'].remove(message.from_user.id)

                    with open('data.txt', 'w') as outfile:
                        json.dump(data, outfile)


                    #db.set_position_balance(message.from_user.id, 0.0)
                    # db.set_position(message.from_user.id, 'position_1m', 'non')
                    # db.set_position(message.from_user.id, 'position_5m', 'non')
                    # db.set_position(message.from_user.id, 'position_15m','non')
                    # db.set_position(message.from_user.id, 'position_30m', 'non')
                    # db.set_position(message.from_user.id, 'position_1h', 'non')
                    # db.set_position(message.from_user.id, 'position_4h', 'non')

                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, 'Trading Bot stopped! ')
                    else:
                        await bot.send_message(message.from_user.id, 'Торговый бот остановлен! ')
                else:
                    Position = db.get_position_balance(message.from_user.id)
                    balance = db.get_deposit_demo(message.from_user.id)
                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, f'Trading Bot stopped!\nBalance: {round(balance, 3)}\nPosition {round(Position, 3)}')
                    else:
                        await bot.send_message(message.from_user.id, f'Торговый бот остановлен!\nBalance: {balance}\nPosition {Position}')
                    # set_position_js(message.from_user.id,'close', True)
                    # time.sleep(10)
                    # db.set_position(message.from_user.id, 'position_1m', 'non')
                    # db.set_position(message.from_user.id, 'position_5m', 'non')
                    # db.set_position(message.from_user.id, 'position_15m','non')
                    # db.set_position(message.from_user.id, 'position_30m', 'non')
                    # db.set_position(message.from_user.id, 'position_1h', 'non')
                    # db.set_position(message.from_user.id, 'position_4h', 'non')
                    del_user_js(message.from_user.id)
                    db.set_start(message.from_user.id, False)

            else:
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'The trading bot has already been stopped! ')
                else:
                    await bot.send_message(message.from_user.id, 'Торговый бот уже Остановлен! ')


        else:
            if db.get_signup(message.from_user.id) == 'setnickname':
                if(len(message.text) > 15):
                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, 'Nickname must not exceed 10 characters')
                    else:
                        await bot.send_message(message.from_user.id, 'Ник не должен привышать 10 символов')
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, 'no_wallet')
                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, 'Nickname registered',  reply_markup=nav.eng_mainMenu)
                    else:
                        await bot.send_message(message.from_user.id, 'Никнейм зарегистрирован успешно!',  reply_markup=nav.mainMenu)
            elif db.get_signup(message.from_user.id) == 'wallet_reg':
                db.set_wallet(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'Done')
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'Wallet registration successful', reply_markup=nav.eng_mainMenu)
                else:
                    await bot.send_message(message.from_user.id, 'Регистрация кошелька прошла успешно', reply_markup=nav.mainMenu)

            elif db.get_signup(message.from_user.id) == 'key_reg':
                db.set_api_key(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'secret_key_reg')

                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'API Key successfully saved')
                    await bot.send_message(message.from_user.id, 'Enter Secret Key')
                else:
                    await bot.send_message(message.from_user.id, 'API Key успешно сохранён')
                    await bot.send_message(message.from_user.id, 'Введите Secret Key:')
            elif db.get_signup(message.from_user.id) == 'secret_key_reg':
                db.set_secret_key(message.from_user.id, message.text)
                db.set_signup(message.from_user.id, 'Done')
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'Secret Key successfully saved', reply_markup=nav.eng_mainMenu)

                else:
                    await bot.send_message(message.from_user.id, 'Secret Key успешно сохранён', reply_markup=nav.mainMenu)


            else:
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'What is this?')
                else:
                    await bot.send_message(message.from_user.id, 'Что это?')
# @dp.message_handler()
# async def start_traid(message: types.Message):
#     elif message.text == '🏁️Запустить':
#         await bot.send_message(message.from_user.id, 'Запуск')
#         tr = Traid(10,dp,bot)
#     elif message.text == '🛑Остановить':
#         pass
#     elif message.text == '⚙️Настройки':
#         pass
@dp.callback_query_handler(text='Tester_sub')
async def Tester_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Tester subscription\nall features available\nwith wallet connection Binance',reply_markup=nav.sub_inlain_Tester)
    else:
        await bot.send_message(message.from_user.id, 'Подписка для тестировщика\nдоступны все функции\nс подключением кошелька Binance', reply_markup=nav.sub_inlain_Tester)

@dp.callback_query_handler(text='Light_sub')
async def Light_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Subscription Light\nDemo account available\nWithout connecting a wallet Binance', reply_markup=nav.sub_inlain_Light)
    else:
        await bot.send_message(message.from_user.id, 'Подписка Лайт\nДоступен демо-счёт\nбез подключения кошелька Binance', reply_markup=nav.sub_inlain_Light)
@dp.callback_query_handler(text='Optimum_sub')
async def Optimum_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Subscription not available, testing in progress')
    else:
        await bot.send_message(message.from_user.id, 'Подписка недоступна, идёт тестирование')
@dp.callback_query_handler(text='Premium_sub')
async def Premium_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Subscription not available, testing in progress')
    else:
        await bot.send_message(message.from_user.id, 'Подписка недоступна, идёт тестирование')
@dp.callback_query_handler(text='Tester_sub')
async def Tester_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Tester subscription\nall features available\nwith wallet connection Binance')
    else:
        await bot.send_message(message.from_user.id, 'Подписка для тестировщика\nдоступны все функции\nс подключением кошелька Binance', reply_markup=nav.sub_inlain_Premium)

@dp.callback_query_handler(text='Tester')
async def Tester(message: types.Message):
    subscription = db.get_subscription(message.from_user.id)
    if subscription == 'Tester':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
            await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')
    else:
        col_tester = db.get_oll_subscription('Tester')
        if len(col_tester) >= 10:
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, f'Maximum limit of testers exceeded\n')
            else:
                await bot.send_message(message.from_user.id, f'Превышен максимальный лимит тестировщиков\n')
        else:
            db.set_subscription(message.from_user.id, 'Tester')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, f'Your subscription has been changed to Tester')
            else:
                await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Tester')
                del_user_js(message.from_user.id)

@dp.callback_query_handler(text='Light')
async def Light(message: types.Message):
    subscription = db.get_subscription(message.from_user.id)

    if subscription == 'Light':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
            await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')
    

    else:
        db.set_subscription(message.from_user.id, 'Light')
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'Your subscription has been changed to Light')
        else:
            await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Light')


@dp.callback_query_handler(text='Optimum')
async def Optimum(message: types.Message):
    subscription = db.get_subscription(message.from_user.id)
    if subscription == 'Optimum':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
           await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')
    elif db.get_wallet(message.from_user.id) == None:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Register your wallet for payment', reply_markup=nav.eng_puyRegWallet)
        else:
            await bot.send_message(message.from_user.id, 'Зарегистрируйте свой кошелёк для оплаты', reply_markup=nav.puyRegWallet)
    else:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id,
                                   f'To connect a subscription for 1 month Optimum\nMake a payment to a cryptocurrency wallet\n5 USDT\nAfter payment, click paid, after confirming the transaction, the package will be connected.\nUSDT Tron Wallet (TRC20)')
        else:
            await bot.send_message(message.from_user.id,
                               f'Для подключения подписки на 1 месяц Optimum\nПроизведите оплату на криптовалютный кошелек\n10 USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции пакет будет подключен.\nКошелек USDT Tron (TRC20)')
        await bot.send_message(message.from_user.id, '\nTSphipuArumtab7EnVHYspUD3bxyLBtaAq', reply_markup=nav.puyMenu_optimum)


@dp.callback_query_handler(text='Premium')
async def Premium(message: types.Message):
    subscription = db.get_subscription(message.from_user.id)
    if subscription == 'Premium':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
            await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')
    elif db.get_wallet(message.from_user.id) == None:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Register your wallet for payment', reply_markup=nav.eng_puyRegWallet)
        else:
            await bot.send_message(message.from_user.id, 'Зарегистрируйте свой кошелёк для оплаты', reply_markup=nav.puyRegWallet)
    else:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id,
                                   f'To connect a subscription for 1 month Premium\nMake a payment to a cryptocurrency wallet\n5 USDT\nAfter payment, click paid, after confirming the transaction, the package will be connected.\nUSDT Tron Wallet (TRC20)')
        else:
            await bot.send_message(message.from_user.id,
                               f'Для подключения подписки на 1 месяц Premium\nПроизведите оплату на криптовалютный кошелек\n50 USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции пакет будет подключен.\nКошелек USDT Tron (TRC20)')
        await bot.send_message(message.from_user.id, '\nTSphipuArumtab7EnVHYspUD3bxyLBtaAq', reply_markup=nav.puyMenu_premium)

@dp.callback_query_handler(text='PuyOk_premium')
async def PuyOk_premium(message: types.Message):
    db.set_payment(message.from_user.id, 'yes')
    db.set_subscription(message.from_user.id, 'Premium')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Your subscription has been changed to Premium')
    else:
        await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Premium')





@dp.callback_query_handler(text='PuyOk_optimum')
async def PuyOk_optimum(message: types.Message):
    db.set_payment(message.from_user.id, 'yes')
    db.set_subscription(message.from_user.id, 'Optimum')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Your subscription has been changed to Premium')
    else:
        await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Optimum')

@dp.callback_query_handler(text='PuyClose_lait_optimum')
async def PuyClose__optimum(message: types.Message):
    db.set_payment(message.from_user.id, 'no')

@dp.callback_query_handler(text='PuyOk_lait')
async def PuyOk_lait(message: types.Message):
    db.set_payment(message.from_user.id, 'yes')
    db.set_subscription(message.from_user.id, 'Light')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Your subscription has been changed to Light')
    else:
        await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Light')

@dp.callback_query_handler(text='minprofitYes')
async def minprofitYes_callb(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_profit_2(callback.from_user.id, 'ON')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Min profit 2% - ON')
        else:
            await callback.answer('Min profit 2% - ON')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='minprofitNo')
async def minprofitNo_callb(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_profit_2(callback.from_user.id, 'OFF')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Min profit 2% - OFF')
        else:
            await callback.answer('Min profit 2% - OFF')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

#********************
@dp.callback_query_handler(text='RsiYes')
async def RsiYes(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_rsi(callback.from_user.id, 'ON')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('RSI - ON')
        else:
            await callback.answer('RSI - ON')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='RsiNo')
async def RsiNo(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_rsi(callback.from_user.id, 'OFF')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('RSI - OFF')
        else:
            await callback.answer('RSI- OFF')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

#********************
@dp.callback_query_handler(text='binance_traidYes')
async def binance_traidYes(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_binance_traid(callback.from_user.id, 'ON')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Connection Binance - ON')
        else:
            await callback.answer('Connection Binance - ON')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='binance_traidNo')
async def binance_traidNo(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_binance_traid(callback.from_user.id, 'OFF')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Connection Binance - OFF')
        else:
            await callback.answer('Connection Binance- OFF')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

#********************
@dp.callback_query_handler(text='averagingYes')
async def averagingYes(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_averaging(callback.from_user.id, 'ON')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Averaging - ON')
        else:
            await callback.answer('Averaging - ON')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='binance_traidNo')
async def binance_traidNo(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_averaging(callback.from_user.id, 'OFF')
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Averaging - OFF')
        else:
            await callback.answer('Averaging- OFF')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='reg_wallet')
async def PuyClose_lait_premium(message: types.Message):
    db.set_signup(message.from_user.id, 'wallet_reg')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Enter your wallet:')
    else:
        await bot.send_message(message.from_user.id, f'Введите ваш кошелёк:')

@dp.callback_query_handler(text='reg_api')
async def PuyClose_lait_premium(message: types.Message):
    db.set_signup(message.from_user.id, 'key_reg')
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('image/1.png', 'Reg_API'))
    media.attach_photo(types.InputFile('image/2.png', 'Reg_API'))
    media.attach_photo(types.InputFile('image/3.png', 'Reg_API'))
    media.attach_photo(types.InputFile('image/4.png', 'Reg_API'))
    #media = [types.InputMediaPhoto('image/1.png', 'Reg_API'), types.InputMediaPhoto('image/1.png'), types.InputMediaPhoto('image/1.png'), types.InputMediaPhoto('image/1.png')]  # Показываем, где фото и как её подписать

    await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото

    #await bot.send_photo(message.from_user.id, photo)
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Enter API Key:')
    else:
        await bot.send_message(message.from_user.id, f'Введите API Key:')

@dp.callback_query_handler(text='reg_nickname')
async def PuyClose_lait_premium(message: types.Message):
    db.set_signup(message.from_user.id, 'setnickname')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, 'Enter your nickname:')
    else:
        await bot.send_message(message.from_user.id, 'Укажите ваш ник:')


@dp.message_handler()
async def bot_masege_user_error(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id,
                               f'    Access tothebot is openonlyfor testers',
                               reply_markup=nav.eng_tradingMenu)

    else:
        await bot.send_message(message.from_user.id,
                               f'Доступ к боту открыт только для тестировщиков',
                               reply_markup=nav.tradingMenu)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)