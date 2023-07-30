
from config import *


import asyncio

from aiogram import Bot, types


CHANNEL_ID = -1005784040512 # это должен быть int, например -1006666666666
def main():
    # строка, чтобы отправить что-нибудь в группу
    await bot.send_message(CHANNEL_ID, 'Hello World')

main()
# запускаем бота
# executor.start_polling(dp)


