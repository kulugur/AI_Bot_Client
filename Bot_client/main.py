import logging
import json
import time
from config import *
from aiogram import Bot, Dispatcher, executor, types
from google.oauth2.credentials import Credentials
from hendlers_fun import position, my_balance, averaging, buy, sell
import markups as nav
from gmail import get_gmail_transfer
from binance.um_futures import UMFutures
from my_binance import balance_binance, get_position, histori_traid, pay_transaction


from binance.error import ClientError
admin = [871610428]


users = [871610428, 634713845, -1001877258339]
def set_admin():
    with open('admin.txt') as json_file:
        data = json.load(json_file)
        data.append(871610428)
        with open('admin.txt', 'w') as outfile:

            json.dump(data, outfile)
def del_admin():

    with open('admin.txt', 'w') as outfile:
        data = []
        json.dump(data, outfile)

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
async def start_admin(message: types.Message):

    db.set_signup(message.from_user.id, 'admin')
    await bot.send_message(message.from_user.id, 'The trading bot is here', reply_markup=nav.bot_link)


    await bot.send_message(message.from_user.id, 'admin', reply_markup=nav.admin_Menu)





@dp.message_handler(lambda message: message.chat.id in admin, commands=['id'])
async def admin_menu(message: types.Message):
    res = message.text.split()
    for i in db.get_all():
        if i[1] == int(res[1]):
            await bot.send_message(message.from_user.id, f'ID: {i[1]}\nName: {i[2]}\nSubscription: {i[5]}\nStart: {i[6]}\nPay_id: {i[9]}\nLenguage: {i[14]}\nDeposit: {i[26]}\nBalance: {i[23]}')

@dp.message_handler(lambda message: message.chat.id in admin, commands=['message'])
async def all_message(message: types.Message):
    text = message.text.split()
    text_mess = ' '.join(text[1:])
    print(text_mess)
    for i in db.get_all():
        try:
            if i[5] != 'Optimum' and i[5] != 'Lite':
                await bot.send_message(i[1], f'Support:\n{text_mess}')
        except:
            pass

@dp.message_handler(lambda message: message.chat.id in admin, commands=['user'])
async def all_user(message: types.Message):
    col_user = 0
    for i in db.get_all():
        col_user += 1
        await bot.send_message(message.from_user.id,
                                   f'Number: {col_user}\nID: {i[1]}\nName:{i[2]}\nSubscription: {i[5]}\nStart: {i[6]}\nPay_id: {i[9]}\nLenguage: {i[14]}\nDeposit: {i[26]}\nBalance: {i[23]}')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if(not db.user_exists(message.from_user.id)):
        start_comand = message.text
        referens_id = str(start_comand[7:])
        if referens_id != '':
            if referens_id != str(message.from_user.id):
                db.add_user(message.from_user.id, referens_id)
                try:
                    await bot.send_message(871610428,
                                           f'новый пользовател {message.from_user.id}\n {message.from_user.mention}\nReferral: {referens_id}')
                    if db.get_language(message.from_user.id) == 'rus':
                        await bot.send_message(referens_id,
                                               f'Новый пользователь зарегистрировался по вашей ссылке\n {message.from_user.mention}')
                    else:
                        await bot.send_message(referens_id,
                                               f'New user registered using your link\n {message.from_user.mention}')
                    deposit = db.get_deposit_demo(referens_id)
                    await bot.send_message(referens_id,
                                           f'{deposit} + 0.5 USDT')
                    deposit += 0.5
                    db.set_deposit_demo(referens_id, deposit)


                except:
                    pass

        else:
            db.add_user(message.from_user.id)
            await bot.send_message(871610428, f'новый пользовател {message.from_user.id}\n {message.from_user.mention}')
        db.set_nickname(message.from_user.id, message.from_user.mention)
        try:
            if message.from_user.locale.language == 'ru':
                db.set_language(message.from_user.id, 'ru')
                await bot.send_message(message.from_user.id,
                                       'Ваш язык определён как Русский изменить можно командой \nEnglish /eng\nRussian /rus')
        except:
            db.set_language(message.from_user.id, 'eng')


        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Welcome to Telegram bot interface\nEnglish /eng\nRussian /rus', reply_markup=nav.eng_mainMenu)
        else:
            await bot.send_message(message.from_user.id, 'Добро пожаловать в Telegram интерфейс бота', reply_markup=nav.mainMenu)
    else:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Main menu!', reply_markup=nav.eng_mainMenu)
        else:
            await bot.send_message(message.from_user.id, 'Главное меню!', reply_markup=nav.mainMenu)

@dp.message_handler(content_types=['photo'])
async def bot_image(message: types):
    if db.get_signup(message.from_user.id) == 'Support':
        for i, photo in enumerate(message.photo):
            try:
                await bot.send_message(871610428, text=f'Support\nuser_id: {message.from_user.id}\n\n{message.text}')
                await bot.send_photo(chat_id=871610428,  photo=photo['file_id'])
                await bot.send_message(message.from_user.id, 'Message sent to support')
                break
            except:
                pass


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
            deposit = db.get_deposit_demo(message.from_user.id)
            subscription = db.get_subscription(message.from_user.id)
            wallet = db.get_wallet(message.from_user.id)
            ref_link = f'{nick_bot}?start={message.from_user.id}'
            my_ref = db.set_referals(message.from_user.id)

            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nNickname: {nicname}\nWallet {wallet}\nYour subscription: {subscription}\nBinance_api: {binance_api}\nDeposit: {deposit} USDT\nReferral link: {ref_link}\nMy referrals: {my_ref}')

            else:
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nНик: {nicname}\nКошелек {wallet}\nВаша подписка: {subscription}\nBinance_api: {binance_api}\nDeposit: {deposit} USDT\nРеферальная ссылка: {ref_link}\nМои рефералы: {my_ref}')
        elif db.get_signup(message.from_user.id) == 'Is_ban':

            if db.get_language(message.from_user.id) == 'ru':
                await bot.send_message(message.from_user.id, 'Вам отказано в доступе к боту!')
            else:
                await bot.send_message(message.from_user.id, 'You are denied access to the bot!')
        elif db.get_signup(message.from_user.id) == 'admin': #Админ панель
            await bot.send_message(message.from_user.id, 'admin панель')
            if message.text == '👣Назад' or message.text == '👣Back':
                db.set_signup(message.from_user.id, 'none')
                db.set_id_help(message.from_user.id,0)
                await bot.send_message(message.from_user.id, '👣', reply_markup=nav.mainMenu)


            elif message.text == 'Enter_position':
                await bot.send_message(message.from_user.id, 'Enter_position', reply_markup=nav.btn_enter_position)
            elif message.text == 'Buy':
                user_id = db.get_id_help(message.from_user.id)
                await buy(user_id)
            elif message.text == 'Sell':
                user_id = db.get_id_help(message.from_user.id)
                await sell(user_id)
            elif message.text == 'Averaging':
                user_id = db.get_id_help(message.from_user.id)
                positino = await averaging(user_id)
                await bot.send_message(message.from_user.id, positino)

            elif message.text == 'Admin_info':
                user_id = db.get_id_help(message.from_user.id)
                positon_user = get_position(db.get_api_key(user_id), db.get_secret_key(user_id))
                histori_user = histori_traid(db.get_api_key(user_id), db.get_secret_key(user_id))
                balane_user = balance_binance(db.get_api_key(user_id), db.get_secret_key(user_id))
                i = len(histori_user) - 20
                for histori in histori_user[i:]:
                    await bot.send_message(message.from_user.id,
                                           f'{histori["symbol"]} {histori["side"]} \n{histori["price"]} {histori["qty"]}\nPNL: {histori["realizedPnl"]}')
                await bot.send_message(message.from_user.id,
                                       f'{positon_user[0]}\nMarketPrice: {positon_user[5]}\nEntry Price: {positon_user[1]}\nSize: {positon_user[2]}\nPNL: {positon_user[3]}\nBalance: {balane_user}')
                try:
                    f = open(f'user_csv/{user_id}.csv', "rb")
                    await bot.send_document(message.from_user.id, f)
                except FileNotFoundError:
                    await bot.send_message(message.from_user.id, text=f'File Not Found Error')
            elif message.text == 'Subscription':
                await bot.send_message(message.from_user.id, f'{db.get_subscription(db.get_id_help(message.from_user.id))}', reply_markup=nav.admin_sub)
            elif message.text == 'Ban':
                db.set_signup(db.get_id_help(message.from_user.id), 'Is_ban')
                del_user_js(db.get_id_help(message.from_user.id))
            elif message.text == "None":
                db.set_subscription(db.get_id_help(message.from_user.id), "None")
                if db.get_language(db.get_id_help(message.from_user.id)) == 'ru':
                    await bot.send_message(message.from_user.id,'Подписка изменена None', reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id),
                                           'Ваша подписка изменена на None!')

                else:
                    await bot.send_message(message.from_user.id,'subscription has been changed to None', reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id), 'Your subscription has been changed to None!')



            elif message.text == "Lite":
                db.set_subscription(db.get_id_help(message.from_user.id), "Lite")
                if db.get_language(db.get_id_help(message.from_user.id)) == 'ru':
                    await bot.send_message(message.from_user.id, 'Подписка изменена Lite', reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id),
                                           'Ваша подписка изменена на Lite!')

                else:
                    await bot.send_message(message.from_user.id, 'subscription has been changed to Lite',
                                           reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id),
                                           'Your subscription has been changed to Lite!')

            elif message.text == "Optimum":
                db.set_subscription(db.get_id_help(message.from_user.id), "Optimum")
                if db.get_language(db.get_id_help(message.from_user.id)) == 'ru':
                    await bot.send_message(message.from_user.id, 'Подписка изменена Optimum', reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id),
                                           'Ваша подписка изменена на Optimum!')

                else:
                    await bot.send_message(message.from_user.id, 'subscription has been changed to Optimum',
                                           reply_markup=nav.admin_Menu)
                    await bot.send_message(db.get_id_help(message.from_user.id),
                                           'Your subscription has been changed to Optimum!')

            elif message.text == 'Найти по ID':
                await bot.send_message(message.from_user.id, 'Enter ID')
                db.set_signup(message.from_user.id, 'admin_id')
                db.set_id_help(message.from_user.id,message.text)
            elif message.text == 'Admin_Support':
                db.set_signup(message.from_user.id, 'admin_support')
                await bot.send_message(message.from_user.id, f'{db.get_user(db.get_id_help(message.from_user.id))}')
                await bot.send_message(message.from_user.id,'Support', reply_markup=nav.btn_support)

            elif message.text == 'Balance':
                await bot.send_message(message.from_user.id,
                                       f'{db.get_deposit_demo(db.get_id_help(message.from_user.id))}',
                                       reply_markup=nav.admin_balance)
            elif message.text == '1$':
                deposit = db.get_deposit_demo(db.get_id_help(message.from_user.id)) + 1
                db.set_deposit_demo(db.get_id_help(message.from_user.id), deposit)
                await bot.send_message(message.from_user.id,
                                       f'{db.get_deposit_demo(db.get_id_help(message.from_user.id))}')
            elif message.text == '5$':
                deposit = db.get_deposit_demo(db.get_id_help(message.from_user.id)) + 5
                db.set_deposit_demo(db.get_id_help(message.from_user.id), deposit)
                await bot.send_message(message.from_user.id,
                                       f'{db.get_deposit_demo(db.get_id_help(message.from_user.id))}')
            elif message.text == '10$':
                deposit = db.get_deposit_demo(db.get_id_help(message.from_user.id)) + 10
                db.set_deposit_demo(db.get_id_help(message.from_user.id), deposit)
                await bot.send_message(message.from_user.id,
                                       f'{db.get_deposit_demo(db.get_id_help(message.from_user.id))}')
            elif message.text == '👣Return':
                await bot.send_message(message.from_user.id, '👣', reply_markup=nav.admin_Menu)
        elif db.get_signup(message.from_user.id) == 'admin_id':
            db.set_id_help(message.from_user.id, message.text)
            user_res = db.get_user(message.text)
            await bot.send_message(message.from_user.id, f'Номер: {user_res[0]}\nID: {user_res[1]}\nИмя: {user_res[2]} \nСтатус: {user_res[4]}\nПодписка: {user_res[5]} \nБаланс: {user_res[26]}\n{user_res[19]}*{user_res[20]}*{user_res[21]}*{user_res[22]}*{user_res[24]}*{user_res[25]}\nПлечо: {user_res[29]}Х')
            db.set_signup(message.from_user.id, 'admin')

        elif db.get_signup(message.from_user.id) == 'admin_support':
            if message.text == 'Exit':
                db.set_signup(message.from_user.id, 'admin')
                await bot.send_message(message.from_user.id, 'EXIT', reply_markup=nav.admin_Menu)
            else:
                await bot.send_message(db.get_id_help(message.from_user.id), f'Support:\n{message.text}')

        elif message.text == '👣Назад' or message.text == '👣Back':
            if db.get_language(message.from_user.id) == 'ru':
                await bot.send_message(message.from_user.id, '👣', reply_markup=nav.mainMenu)


            else:
                await bot.send_message(message.from_user.id,'👣', reply_markup=nav.eng_mainMenu)
        elif message.text == '📲Support' or message.text == '📲Поддержка':
            db.set_signup(message.from_user.id, 'Support')
            if db.get_language(message.from_user.id) == 'ru':
                await bot.send_message(message.from_user.id, '📲\nОтправьте сообщение в поддержку', reply_markup=nav.btn_support)

            else:
                await bot.send_message(message.from_user.id, '📲\nSend a message to support', reply_markup=nav.btn_support)
        elif db.get_signup(message.from_user.id) == 'Support':

            if message.text == 'Exit':
                db.set_signup(message.from_user.id, 'none')
                if db.get_language(message.from_user.id) == 'ru':
                    await bot.send_message(message.from_user.id, '👣', reply_markup=nav.mainMenu)


                else:
                    await bot.send_message(message.from_user.id,'👣', reply_markup=nav.eng_mainMenu)
            else:
                await bot.send_message(871610428, text=f'Support\nuser_id: {message.from_user.id}\n/admin\n{message.text}')

                await bot.send_message(message.from_user.id, 'Message sent to support')


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
        elif message.text == '💵️Deposit':
            deposit = db.get_deposit_demo(message.from_user.id)
            await bot.send_message(message.from_user.id, f'Deposit: {deposit} USDT')
            if db.get_wallet(message.from_user.id) == None:
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'Register your Binance Pay for payment',
                                       reply_markup=nav.eng_registr)
                else:
                    await bot.send_message(message.from_user.id, 'Зарегистрируйте свой Binance Pay для оплаты',
                                       reply_markup=nav.eng_registr)
            else:
                media = types.MediaGroup()
                media.attach_photo(types.InputFile('image/photo_2023-04-09_17-38-53.jpg', 'Pay_ID'))
                await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id,
                                           f'USDT\nAfter payment, click paid, after confirming the transaction, The balance will be replenished.\nUSDT Pay ID wallet: 210914309', reply_markup=nav.eng_puyMenu)
                else:
                    await bot.send_message(message.from_user.id,
                                           f'USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции Баланс будет пополнен.\nКошелек USDT Pay ID: 210914309', reply_markup=nav.puyMenu_Ok)


        elif message.text == 'ℹ️Инфо' or  message.text == 'ℹ️Info':
            await bot.send_message(message.from_user.id, 'ℹ️')
            nicname = db.get_nickname(message.from_user.id)
            timeSub = db.get_time_sub(message.from_user.id)
            subscription = db.get_subscription(message.from_user.id)
            wallet = db.get_wallet(message.from_user.id)
            video = open('video/QuickStart.mp4', 'rb')

            if db.get_api_key(message.from_user.id) != None and db.get_secret_key(message.from_user.id) != None:
                binance_api = 'Yes'
            else:
                binance_api = 'No'
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nNickname: {nicname}\nWallet: {wallet}\nBinance_api: {binance_api}\nYour subscription: {subscription}\nLeft: {timeSub} days\nMain group:https://t.me/ai_binance_trading\nDevelopment support: https://t.me/+VWFxrDjnK59kMTM6')
                await bot.send_message(message.from_user.id, '\nVideo loading quick start!')
                await bot.send_video(message.from_user.id, video)
            else:
                await bot.send_message(message.from_user.id,
                                       f'User_id: {message.from_user.id}\nНик: {nicname}\nКошелек: {wallet}\nBinance_api: {binance_api}\nВаша подписка: {subscription}\nОсталось: {timeSub} дней\nГлавная группа:https://t.me/ai_binance_trading\nРазработка поддержка: https://t.me/ai_trade_rus\nИдёт загрузка видео быстрый старт!')
                await bot.send_message(message.from_user.id,'\nИдёт загрузка видео быстрый старт!')
                await bot.send_video(message.from_user.id, video)

        elif  db.get_subscription(message.from_user.id) == "None" and db.get_signup(message.from_user.id) != 'wallet_reg':
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,'✍')
                await bot.send_message(message.from_user.id, f'Your subscription: {db.get_subscription(message.from_user.id)}', reply_markup=nav.puyMenu)

            else:
                await bot.send_message(message.from_user.id, '✍')
                await bot.send_message(message.from_user.id, f'Ваша подписка: {db.get_subscription(message.from_user.id)}', reply_markup=nav.puyMenu)

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

            # await bot.send_message(message.from_user.id, '*****************************', reply_markup=nav.sub_inlain_Premium)
            # await bot.send_message(message.from_user.id, 'Подписка Премиум\nдоступны все функции\nс подключением кошелька')
        elif message.text == '📈️Торговля' or  message.text == '📈️Trading':
            await bot.send_message(message.from_user.id, '📈️')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, f'Your subscription {db.get_subscription(message.from_user.id)}\nTo exit to the Main Menu, enter 👣Back', reply_markup=nav.eng_tradingMenu)

            else:
                await bot.send_message(message.from_user.id, f'Ваша подписка {db.get_subscription(message.from_user.id)}\nДля возврата нажмите 👣Back', reply_markup=nav.tradingMenu)



        elif message.text == '⚙️Дополнительные команды' or  message.text == '⚙️Additional commands':
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, '⚙️Additional commands', reply_markup=nav.eng_addParam)
            else:
                await bot.send_message(message.from_user.id, '⚙️Additional commands', reply_markup=nav.eng_addParam)
        elif message.text == 'Position':

            t = await position(message.from_user.id)
            print(t)
        elif message.text == 'Get Excel':
            try:
                f = open(f'user_csv/{message.from_user.id}.csv', "rb")
                await bot.send_document(message.from_user.id, f)
            except FileNotFoundError:
                await bot.send_message(message.from_user.id, text=f'File Not Found Error')

        elif message.text == 'Balance':
            await my_balance(message.from_user.id)

        elif message.text == 'Last order':
            subscription = db.get_subscription(message.from_user.id)
            if subscription == 'Lite':

                id_key = admin[0]
            else:

                id_key = message.from_user.id
            key = db.get_api_key(id_key)
            secret = db.get_secret_key(id_key)
            if key != None or secret != None and subscription != 'Lite' :
                try:
                    histori = histori_traid(key, secret)[-1]
                except:
                    await bot.send_message(message.from_user.id,'Binance API Error', reply_markup= nav.eng_registr)
                if type(histori) is str:
                    await bot.send_message(message.from_user.id, text=f'ERROR: API-KEY Futures',
                                           reply_markup=nav.eng_registr)
                else:
                    await bot.send_message(message.from_user.id, f'{histori["symbol"]}\n{histori["side"]}\nBTC: {histori["qty"]}BTC\nPrice: {histori["price"]}\ncommission: {histori["commission"]}')
            else:
                await bot.send_message(message.from_user.id, 'No Binance API', reply_markup= nav.eng_registr)

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
                await bot.send_message(message.from_user.id, '*         Leverage           *', reply_markup=nav.settingbinance_traid)
            else:
                await bot.send_message(message.from_user.id, '*    Кредитное плечо   *', reply_markup=nav.settingbinance_traid)




        elif message.text == '🏁️Запустить' or  message.text == '🏁️Start':
            await bot.send_message(message.from_user.id, '🏁️')
            if not db.get_start(message.from_user.id):
                subscript = db.get_subscription(message.from_user.id)
                if subscript != 'Lite':
                    try:
                        await my_balance(message.from_user.id)

                        test = balance_binance(db.get_api_key(message.from_user.id), db.get_secret_key(message.from_user.id))
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
                        leverage = db.get_leverage(message.from_user.id)
                        if leverage == 1.5:
                            leverage = 'Auto(Standard)'
                        if db.get_language(message.from_user.id) == 'eng':


                            await bot.send_message(message.from_user.id, f'The trading bot is ready to run Check the settings!\nParameters:\nRSI: {db.get_rsi(message.from_user.id)}\nmin profit 2%: {db.get_profit_2(message.from_user.id)}\nAveraging: {db.get_averaging(message.from_user.id)}\nConnection Binance: {db.get_binance_traid(message.from_user.id)}\nLeverage: {leverage}\nBot balance: {db.get_deposit_demo(message.from_user.id)}', reply_markup=nav.eng_run_bot)
                        else:
                            await bot.send_message(message.from_user.id, f'Торговый бот готов к запуску Проверьте настройки\nПараметры:\nRSI: {db.get_rsi(message.from_user.id)}\nmin profit 2%: {db.get_profit_2(message.from_user.id)}\nAveraging: {db.get_averaging(message.from_user.id)}\nConnection Binance: {db.get_binance_traid(message.from_user.id)}\nКредитное плечо: {leverage}\nБаланс Бот: {db.get_deposit_demo(message.from_user.id)}', reply_markup=nav.eng_run_bot)


                else:
                    #db.set_position_balance(message.from_user.id, 0.00000001)
                    set_user_js(message.from_user.id)

                    db.set_start(message.from_user.id, True)
                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, f'The trading bot is running!\nSubscription {subscript}')
                    else:
                        await bot.send_message(message.from_user.id, f'Торговый бот запущен!\nПодписка  {subscript}')

            else:
                if db.get_language(message.from_user.id) == 'eng':
                    await bot.send_message(message.from_user.id, 'The trading bot is already running! ')
                else:
                    await bot.send_message(message.from_user.id, 'Торговый бот уже запущен! ')

        elif message.text == '🛑Остановить' or  message.text == '🛑Stop':
            await bot.send_message(message.from_user.id, '🛑')
            if db.get_start(message.from_user.id):
                if db.get_subscription(message.from_user.id) != 'Lite':
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

                    if db.get_language(message.from_user.id) == 'eng':
                        await bot.send_message(message.from_user.id, f'Trading Bot stopped!')

                    else:
                        await bot.send_message(message.from_user.id, f'Торговый бот остановлен!')


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
                    await bot.send_message(message.from_user.id, 'Binance Pay registration successful!', reply_markup=nav.puyMenu)
                else:
                    await bot.send_message(message.from_user.id, 'Регистрация Binance Pay прошла успешно! ', reply_markup=nav.puyMenu)

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
@dp.callback_query_handler(text='run_bot')
async def run_bot(message: types.Message):
    db.set_start(message.from_user.id, True)
    with open('data.txt') as json_file:
        data = json.load(json_file)
        data['user_id'].append(message.from_user.id)

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    await bot.send_message(message.from_user.id, 'Trading bot launched')
@dp.callback_query_handler(text='Tester_sub')
async def Tester_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Tester subscription\nall features available\nwith wallet connection Binance',reply_markup=nav.sub_inlain_Tester)
    else:
        await bot.send_message(message.from_user.id, 'Подписка для тестировщика\nдоступны все функции\nс подключением кошелька Binance', reply_markup=nav.sub_inlain_Tester)

@dp.callback_query_handler(text='Light_sub')
async def Light_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Subscription Lite\nWithout connecting a wallet Binance\nprice Free.', reply_markup=nav.sub_inlain_Light)
    else:
        await bot.send_message(message.from_user.id, 'Подписка Лайт\nбез подключения кошелька Binance\nцена бесплатно.', reply_markup=nav.sub_inlain_Light)
@dp.callback_query_handler(text='Optimum_sub')
async def Optimum_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Binance wallet connection\navailable with Optimum\nsubscriptionthe price of 15 USDT.\nBot commission 15% of your profit!', reply_markup=nav.sub_inlain_Optimum)
    else:
        await bot.send_message(message.from_user.id, 'Подключение кошелька Binance\nдоступно с подпиской Optimum\nцена 15 USDT и.\nКомиссия бота 15% от вашей прибыли!', reply_markup=nav.sub_inlain_Optimum)
@dp.callback_query_handler(text='Premium_sub')
async def Premium_sub(message: types.Message):
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id,
                               f'Binance wallet connection\navailable with Premium\nsubscriptionthe price of 30 USDT.\nBot commission 15% of your profit!',
                               reply_markup=nav.sub_inlain_Premium)
    else:
        await bot.send_message(message.from_user.id,
                               'Подключение кошелька Binance\nдоступно с подпиской Premium\nцена 30 USDT \nКомиссия бота 15% от вашей прибыли!',
                               reply_markup=nav.sub_inlain_Premium)
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
        if len(col_tester) >= 1:
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

@dp.callback_query_handler(text='Lite')
async def Light(message: types.Message):
    subscription = db.get_subscription(message.from_user.id)

    if subscription == 'Lite':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
            await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')
    elif subscription == 'Optimum':
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, f'You already have a subscription {subscription}')
        else:
            await bot.send_message(message.from_user.id, f'У вас уже подключена подписка {subscription}')


    else:
        db.set_subscription(message.from_user.id, 'Lite')
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id, 'Your subscription has been changed to Lite')
        else:
            await bot.send_message(message.from_user.id, 'Ваша подписка изменено на lite')
        # else:
        #     media = types.MediaGroup()
        #     media.attach_photo(types.InputFile('image/photo_2023-04-09_17-38-53.jpg', 'Pay_ID'))
        #     await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото
        #     if db.get_language(message.from_user.id) == 'eng':
        #         await bot.send_message(message.from_user.id,
        #                                    f'Your balance: {db.get_deposit_demo(message.from_user.id)}\nAfter payment, click paid, after confirming the transaction, The balance will be replenished.\nUSDT Pay ID wallet: 210914309',
        #                                    reply_markup=nav.eng_puyMenu)
        #     else:
        #         await bot.send_message(message.from_user.id,
        #                                    f'Ваш баланс: {db.get_deposit_demo(message.from_user.id)} USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции Баланс будет пополнен.\nКошелек USDT Pay ID: 210914309',
        #                                    reply_markup=nav.puyMenu_Ok)




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
            await bot.send_message(message.from_user.id, 'Register your Binance Pay for payment', reply_markup=nav.eng_registr)
        else:
            await bot.send_message(message.from_user.id, 'Зарегистрируйте свой Binance Pay для оплаты', reply_markup=nav.eng_registr)
    else:
        if db.get_deposit_demo(message.from_user.id) >= 15:
            deposit = db.get_deposit_demo(message.from_user.id) - 15
            db.set_deposit_demo(message.from_user.id, deposit)
            db.set_subscription(message.from_user.id,'Optimum')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'Your subscription has been changed to Optimum\nBot balance: {db.get_deposit_demo(message.from_user.id)}$')
            else:

                await bot.send_message(message.from_user.id,
                                       f'Ваша подписка изменено на Optimum\nБаланс бота: {db.get_deposit_demo(message.from_user.id)}$')
        else:
            media = types.MediaGroup()
            media.attach_photo(types.InputFile('image/photo_2023-04-09_17-38-53.jpg', 'Pay_ID'))
            await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'Your balance: {db.get_deposit_demo(message.from_user.id)} USDT\nAfter payment, click paid, after confirming the transaction, The balance will be replenished.\nUSDT Pay ID wallet: 210914309',
                                       reply_markup=nav.eng_puyMenu)
            else:
                await bot.send_message(message.from_user.id,
                                       f'Ваш баланс: {db.get_deposit_demo(message.from_user.id)} USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции Баланс будет пополнен.\nКошелек USDT Pay ID: 210914309',
                                       reply_markup=nav.puyMenu_Ok)


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
            await bot.send_message(message.from_user.id, 'Register your Binance Pay for payment',
                                   reply_markup=nav.eng_registr)
        else:
            await bot.send_message(message.from_user.id, 'Зарегистрируйте свой Binance Pay для оплаты',
                                   reply_markup=nav.eng_registr)
    else:
        if db.get_deposit_demo(message.from_user.id) >= 30:
            deposit = db.get_deposit_demo(message.from_user.id) - 30
            db.set_deposit_demo(message.from_user.id, deposit)
            db.set_subscription(message.from_user.id, 'Premium')
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id, f'Your subscription has been changed to Premium\nBot balance: {db.get_deposit_demo(message.from_user.id)}$')
            else:

                await bot.send_message(message.from_user.id, f'Ваша подписка изменено на Premium\nБаланс бота: {db.get_deposit_demo(message.from_user.id)}$')
        else:
            media = types.MediaGroup()
            media.attach_photo(types.InputFile('image/photo_2023-04-09_17-38-53.jpg', 'Pay_ID'))
            await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото
            if db.get_language(message.from_user.id) == 'eng':
                await bot.send_message(message.from_user.id,
                                       f'Your balance: {db.get_deposit_demo(message.from_user.id)} USDT\nAfter payment, click paid, after confirming the transaction, The balance will be replenished.\nUSDT Pay ID wallet: 210914309',
                                       reply_markup=nav.eng_puyMenu)
            else:
                await bot.send_message(message.from_user.id,
                                       f'Ваш баланс: {db.get_deposit_demo(message.from_user.id)} USDT\nПосле оплаты нажмите оплатил, после подтверждения транзакции Баланс будет пополнен.\nКошелек USDT Pay ID: 210914309',
                                       reply_markup=nav.puyMenu_Ok)

@dp.callback_query_handler(text='PuyOk_premium')
async def PuyOk_premium(message: types.Message):

    db.set_subscription(message.from_user.id, 'Premium')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Your subscription has been changed to Premium')
    else:
        await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Premium')


@dp.callback_query_handler(text='PuyOk')
async def PuyOk(message: types.Message):
    key = 'CCW3X4P0vvL3PWpQdN0ZUiivCSTvEuU6Xl6m5UkCHP75oxc0bHKyN9viNnQhzH0M'
    secret = 'EnWsq6BhNIUagMUA5PmmAa1Ea3r2WfB8VhZCwIzmEx6O8MmASwOpRbvOOd02g4S3'
    pay = pay_transaction(key, secret, db.get_wallet(message.from_user.id))
    await bot.send_message(admin[0],
                           f'Ожидаем подтверждение транзакций от\n{message.from_user.id}')
    if pay[0] != str(db.get_payment(message.from_user.id)):
        db.set_payment(message.from_user.id,pay[0])
        deposit = db.get_deposit_demo(message.from_user.id) + float(pay[1])
        db.set_deposit_demo(message.from_user.id, deposit)
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id,
                                   f'Replenishment of balance.\ndeposit: {deposit}')

        else:
            await bot.send_message(message.from_user.id,
                                   f'Пополнение баланса.\nДепозит{deposit}')
    else:
        if db.get_language(message.from_user.id) == 'eng':
            await bot.send_message(message.from_user.id,
                                   f'Waiting for transaction confirmation')

        else:
            await bot.send_message(message.from_user.id,
                                   f'Ожидаем подтверждение транзакций')


@dp.callback_query_handler(text='PuyOk_optimum')
async def PuyOk_optimum(message: types.Message):

    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id,
                           f'Waiting for transaction confirmation')

    else:
        await bot.send_message(message.from_user.id,
                       f'Ожидаем подтверждение транзакций')





@dp.callback_query_handler(text='PuyOk_lait')
async def PuyOk_lait(message: types.Message):

    db.set_subscription(message.from_user.id, 'Lite')
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Your subscription has been changed to Lite')
    else:
        await bot.send_message(message.from_user.id, f'Ваша подписка изменена на Lite')

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

@dp.callback_query_handler(text='Auto(Standard)')
async def auto_Standard(callback: types.CallbackQuery):
    subscription = db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 1.5)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: Auto(Standard)')
            await bot.send_message(callback.from_user.id, f'Leverage changed: Auto(Standard)\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: Auto(Standard)')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: Auto(Standard)\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='leverage_5x')
async def leverage_5x(callback: types.CallbackQuery):
    subscription = db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 5)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: 5X')
            await bot.send_message(callback.from_user.id, f'Leverage changed: 5X\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: 5X')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: 5X\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')

@dp.callback_query_handler(text='leverage_10x')
async def leverage_10x(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 10)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: 10X')
            await bot.send_message(callback.from_user.id,
                                   f'Leverage changed: 10X\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: 10X')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: 10X\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')
@dp.callback_query_handler(text='leverage_15x')
async def leverage_15x(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 15)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: 15X')
            await bot.send_message(callback.from_user.id,
                                   f'Leverage changed: 15X\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: 15X')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: 15X\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')
    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')
@dp.callback_query_handler(text='leverage_20x')
async def leverage_20x(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 10)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: 20X')
            await bot.send_message(callback.from_user.id,
                                   f'Leverage changed: 20X\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: 20X')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: 20X\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')

    else:
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Premium subscription required')
        else:
            await callback.answer('Нужена Premium подписка')
@dp.callback_query_handler(text='leverage_25x')
async def leverage_25x(callback: types.CallbackQuery):
    subscription =db.get_subscription(callback.from_user.id)
    if subscription == 'Tester' or subscription == 'Premium':
        db.set_leverage(callback.from_user.id, 10)
        if db.get_language(callback.from_user.id) == 'eng':
            await callback.answer('Leverage changed: 25X')
            await bot.send_message(callback.from_user.id,
                                   f'Leverage changed: 25X\nIncreasing leverage leads to additional risk you balance must be at least $200!')
        else:
            await callback.answer('Кредитное плечо изменено: 25X')
            await bot.send_message(callback.from_user.id,
                                   f'Кредитное плечо изменено: 25X\nУвеличение кредитного плеча приводит к дополнительному риску, ваш баланс должен быть не менее 200 долларов!')
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
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('image/photo_2023-04-09_17-38-46.jpg', 'Pay_ID'))
    media.attach_photo(types.InputFile('image/photo_2023-04-09_17-37-24.jpg', 'Pay_ID'))
    await bot.send_media_group(message.from_user.id, media=media)  # Отправка фото
    if db.get_language(message.from_user.id) == 'eng':
        await bot.send_message(message.from_user.id, f'Enter your Pay-ID:')

    else:
        await bot.send_message(message.from_user.id, f'Введите ваш Pay-ID:')

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