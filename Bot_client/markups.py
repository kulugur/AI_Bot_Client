from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

eng_deposit = KeyboardButton(text='💵️Deposit')
#RUS
btn_back = KeyboardButton(text='👣Назад')

btn_exit = KeyboardButton(text='Exit')
btn_support = ReplyKeyboardMarkup(resize_keyboard=True)
btn_support.add(btn_exit)
admin_back = KeyboardButton(text='👣Return')
admin_id = KeyboardButton(text='Найти по ID')
admin_sub = KeyboardButton(text='Subscription')
admin_balance = KeyboardButton(text='Balance')
admin_info = KeyboardButton(text='Admin_info')
enter_position = KeyboardButton(text='Enter_position')
admin_support = KeyboardButton(text='Admin_Support')
admin_ban = KeyboardButton(text='Ban')
admin_Menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_Menu.add(admin_id,admin_sub,admin_balance,admin_support, admin_info,enter_position, admin_ban, btn_back)
btn_enter_position = ReplyKeyboardMarkup(resize_keyboard=True)
admin_buy = KeyboardButton(text='Buy')
admin_sell = KeyboardButton(text='Sell')
admin_Averaging = KeyboardButton(text='Averaging')
btn_enter_position.add(admin_buy, admin_sell, admin_Averaging, admin_back)

admin_sub_liht = KeyboardButton(text='Lite')
admin_sub_optima = KeyboardButton(text='Optimum')
admin_sub_none = KeyboardButton(text='None')
admin_sub = ReplyKeyboardMarkup(resize_keyboard=True)
admin_sub.add(admin_sub_none, admin_sub_liht, admin_sub_optima, admin_back)

admin_balance_1 = KeyboardButton(text='1$')
admin_balance_5 = KeyboardButton(text='5$')
admin_balance_10 = KeyboardButton(text='10$')
admin_balance = ReplyKeyboardMarkup(resize_keyboard=True)
admin_balance.add(admin_balance_1, admin_balance_5, admin_balance_10, admin_back)



btnProfile = KeyboardButton('👽 Профиль')
btnSub = KeyboardButton('✍️Подписка')
btnTrading = KeyboardButton('📈️Торговля')
btninfo = KeyboardButton(text='ℹ️Инфо')
btnSettings = KeyboardButton('⚙️Настройки')
btnSupport = KeyboardButton(text='📲Поддержка')
btnAdd_commands = KeyboardButton('⚙️Дополнительные команды')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub, btnTrading,btninfo, btnSupport, btnSettings)

btnOptions = KeyboardButton('🤖Параметры')
btnStart = KeyboardButton('🏁️Запустить')
btnStop = KeyboardButton('🛑Остановить')

tradingMenu = ReplyKeyboardMarkup(resize_keyboard=True)
tradingMenu.add(btnOptions, btnStart, btnStop, btnAdd_commands,btn_back)

btnPuyOk = InlineKeyboardButton(text='💵Оплачено', callback_data='PuyOk')
puyMenu_Ok = InlineKeyboardMarkup(row_width=1)
puyMenu_Ok.add(btnPuyOk)

btn_bot_link = InlineKeyboardButton(text='Bot',url='https://t.me/Ai_Trader_client_bot')
bot_link = InlineKeyboardMarkup(row_width=1)
bot_link.add(btn_bot_link)
btnPuyOk_lait = InlineKeyboardButton(text='💵Оплачено', callback_data='PuyOk_lait')
puyMenu_lait = InlineKeyboardMarkup(row_width=1)
puyMenu_lait.add(btnPuyOk_lait)

btnPuyOk_optimum = InlineKeyboardButton(text='💵Оплачено', callback_data='PuyOk_optimum')
puyMenu_optimum = InlineKeyboardMarkup(row_width=1)
puyMenu_optimum.add(btnPuyOk_optimum)

btnPuyOk_premium = InlineKeyboardButton(text='💵Оплачено', callback_data='PuyOk_premium')
puyMenu_premium = InlineKeyboardMarkup(row_width=1)
puyMenu_premium.add(btnPuyOk_premium)

btnRegWallet = KeyboardButton(text='📝Регистрация')
btninfo = KeyboardButton(text='ℹ️Инфо')

puyRegWallet = ReplyKeyboardMarkup(resize_keyboard=True)
puyRegWallet.add(btnRegWallet, eng_deposit, btn_back)

btnTester = InlineKeyboardButton(text='OK', callback_data='Tester')
btnLight = InlineKeyboardButton(text='OK', callback_data='Lite')
btnOptimum = InlineKeyboardButton(text='OK', callback_data='Optimum')
btnPremium = InlineKeyboardButton(text='OK', callback_data='Premium')
sub_inlain_Tester = InlineKeyboardMarkup(row_width=1)
sub_inlain_Light = InlineKeyboardMarkup(row_width=1)
sub_inlain_Optimum = InlineKeyboardMarkup(row_width=1)
sub_inlain_Premium = InlineKeyboardMarkup(row_width=1)
sub_inlain_Tester.add(btnTester)
sub_inlain_Light.add(btnLight)
sub_inlain_Optimum.add(btnOptimum)
sub_inlain_Premium.add(btnPremium)

btnTester_sub = InlineKeyboardButton(text='Tester', callback_data='Tester_sub')
btnLight_sub = InlineKeyboardButton(text='Lite', callback_data='Light_sub')
btnOptimum_sub = InlineKeyboardButton(text='Optimum', callback_data='Optimum_sub')
btnPremium_sub = InlineKeyboardButton(text='Premium', callback_data='Premium_sub')
puyMenu = InlineKeyboardMarkup(row_width=1)
puyMenu.add(btnTester_sub, btnLight_sub, btnOptimum_sub, btnPremium_sub)

btnminprofitYes = InlineKeyboardButton(text='Yes', callback_data='minprofitYes')
btnminprofitNo = InlineKeyboardButton(text='No', callback_data='minprofitNo')
settingProfit = InlineKeyboardMarkup(row_width=1)
settingProfit.row(btnminprofitYes, btnminprofitNo)

btnRsiYes = InlineKeyboardButton(text='Yes', callback_data='RsiYes')
btnRsiNo = InlineKeyboardButton(text='No', callback_data='RsiNo')
settingRSI = InlineKeyboardMarkup(row_width=1)
settingRSI.row(btnRsiYes, btnRsiNo)

btn_leverage_Auto_Standard = InlineKeyboardButton(text='Auto(Standard)', callback_data='Auto(Standard)')
btn_leverage_5x = InlineKeyboardButton(text='5x', callback_data='leverage_5x')
btn_leverage_10x = InlineKeyboardButton(text='10x', callback_data='leverage_10x')
btn_leverage_15x = InlineKeyboardButton(text='15x', callback_data='leverage_15x')
btn_leverage_20x = InlineKeyboardButton(text='20x', callback_data='leverage_20x')
btn_leverage_25x = InlineKeyboardButton(text='25x', callback_data='leverage_25x')
settingbinance_traid = InlineKeyboardMarkup(row_width=1)
settingbinance_traid.row(btn_leverage_Auto_Standard, btn_leverage_5x, btn_leverage_10x, btn_leverage_15x, btn_leverage_20x, btn_leverage_25x)

btnAveragingYes = InlineKeyboardButton(text='Yes', callback_data='averagingYes')
btnAveragingNo = InlineKeyboardButton(text='No', callback_data='averagingNo')
settingAveraging = InlineKeyboardMarkup(row_width=1)
settingAveraging.row(btnAveragingYes, btnAveragingNo)



#ENG
eng_btn_run_bot = KeyboardButton(text='Run Bot')
eng_btn_back = KeyboardButton(text='👣Back')
eng_btnProfile = KeyboardButton('👽 Profile')
eng_btnSub = KeyboardButton('✍️Subscribe')
eng_btnTrading = KeyboardButton('📈️Trading')
eng_btninfo = KeyboardButton(text='ℹ️Info')
eng_btnSupport = KeyboardButton(text='📲Support')
eng_btnSettings = KeyboardButton('⚙️Settings')
eng_btnAdd_commands = KeyboardButton('⚙️Additional commands')
eng_mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
eng_mainMenu.add(eng_btnProfile, eng_btnSub, eng_btnTrading, eng_btninfo,eng_btnSupport, eng_btnSettings)

eng_btnOptions = KeyboardButton('🤖Options')
eng_btnStart = KeyboardButton('🏁️Start')
eng_btnStop = KeyboardButton('🛑Stop')
eng_tradingMenu = ReplyKeyboardMarkup(resize_keyboard=True)
eng_tradingMenu.add(eng_btnOptions, eng_btnStart, eng_btnStop, eng_btnAdd_commands,eng_btn_back)


eng_btnPuyOk_light = InlineKeyboardButton(text='💵Paid', callback_data='PuyOk_lait')
eng_puyMenu_light = InlineKeyboardMarkup(row_width=1)
eng_puyMenu_light.add(eng_btnPuyOk_light)

eng_btn_run_bot = InlineKeyboardButton(text='Run Bot', callback_data='run_bot')
eng_run_bot = InlineKeyboardMarkup(row_width=1)
eng_run_bot.add(eng_btn_run_bot)


eng_btnPuyOk = InlineKeyboardButton(text='💵Paid', callback_data='PuyOk')
eng_puyMenu = InlineKeyboardMarkup(row_width=1)
eng_puyMenu.add(eng_btnPuyOk)


eng_btnPuyOk_optimum = InlineKeyboardButton(text='💵Paid', callback_data='PuyOk_optimum')
eng_puyMenu_optimum = InlineKeyboardMarkup(row_width=1)
eng_puyMenu_optimum.add(eng_btnPuyOk_optimum)

eng_btnPuyOk_premium = InlineKeyboardButton(text='💵Paid', callback_data='PuyOk_premium')
eng_puyMenu_premium = InlineKeyboardMarkup(row_width=1)
eng_puyMenu_premium.add(eng_btnPuyOk_premium)

eng_btnRegWallet = KeyboardButton(text='📝Registration')
eng_btninfo = KeyboardButton(text='ℹ️Info')

eng_puyRegWallet = ReplyKeyboardMarkup(resize_keyboard=True)
eng_puyRegWallet.add(eng_btnRegWallet, eng_deposit, eng_btn_back)

eng_reg_wallet = InlineKeyboardButton(text='Binance-Pay-ID', callback_data='reg_wallet')
eng_reg_api = InlineKeyboardButton(text='Binance API', callback_data='reg_api')
eng_reg_nickname = InlineKeyboardButton(text='Nickname', callback_data='reg_nickname')
eng_registr = InlineKeyboardMarkup(row_width=1)
eng_registr.add(eng_reg_wallet, eng_reg_api,eng_reg_nickname)

eng_get_position = KeyboardButton(text='Position')
eng_get_balance = KeyboardButton(text='Balance')
eng_get_order = KeyboardButton(text='Last order')
eng_get_excel = KeyboardButton(text='Get Excel')
eng_addParam = ReplyKeyboardMarkup(resize_keyboard=True)
eng_addParam.add(eng_get_position, eng_get_balance, eng_get_order, eng_get_excel, eng_btn_back)





