
from aiogram import Bot, Dispatcher, executor, types

from db import Database

tg_chanel_user = 871610428
TOKEN = '5202575933:AAF-q7yxh_EyQBqsYtiuIViIFUHh27SFY0A'
channel_id = "-1001702093331"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')