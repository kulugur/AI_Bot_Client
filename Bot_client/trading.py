
import time
import json
from binance.um_futures import UMFutures
import numpy as np

# Initialize the Binance client
client = UMFutures()
symbol = 'BTCUSDT'
interval = '1m'
#channel_id = "871610428"  # The channel ID starts with a - and is followed by the channel's unique ID
import telebot

bot = telebot.bot = telebot.TeleBot(token="5202575933:AAF-q7yxh_EyQBqsYtiuIViIFUHh27SFY0A")
# Initialize the Telegram bot


# Set the channel ID
#channel_id = [5612997951]  # The channel ID starts with a - and is followed by the channel's unique ID


# Send the message

print('Start')
def channel_enter(client, interval,PROFIT_FLAG,FLAG, enter):
    # Set the trading pair, amount, leverage and period
    symbol = 'BTCUSDT'
    amount = 1
    leverage = 125

    # Fetch historical data
    ohlcv = client.klines("BTCUSDT", interval, limit=500)

    closes = [float(x[4]) for x in ohlcv]

    # Calculate upper and lower channel boundaries
    sma = np.mean(closes, dtype=float)
    std = np.std(closes, dtype=float)
    upper = sma + 2 * std
    lower = sma - 2 * std
    with open('data.txt') as json_file:
        data = json.load(json_file)
        channel_id = data['user_id']


    print(channel_id)
    # Get the current ticker price
    ticker = client.ticker_price(symbol)
    last_price = float(ticker['price'])
    #print(upper, interval)
    #print(lower, interval)
    profit_pricent = (upper/lower * 100) - 100
    profit = 0
    # Implement the strategy
    if last_price > upper and FLAG != 'short' and profit_pricent >= 2:
        if PROFIT_FLAG:
            for i in channel_id:
                bot.send_message(chat_id=i,
                              text=f'Closing price {interval}\n{last_price}\n Profit {last_price - enter}')
            #print(f'Closing price {last_price}\n Profit { last_price - enter}')
            profit = last_price - enter
            FLAG = None

        FLAG = 'short'
        #print("Продано по", last_price, "так как выше верхней границы канала")
        enter = last_price
        for i in channel_id:
            bot.send_message(chat_id=i, text=f"Position enter {interval}\n {enter}\n SHORT")
        PROFIT_FLAG = True




    elif last_price < lower and  FLAG != 'long' and profit_pricent >= 2:
        if PROFIT_FLAG:
            for i in channel_id:
                bot.send_message(chat_id=i,
                              text=f'Closing price {interval}\n{last_price}\nProfit {enter - last_price}')
            #print(f'Closing price {interval}\n{last_price}\n Profit {enter - last_price}')
            profit = enter - last_price
            FLAG = None

        FLAG = 'long'
        #print("Куплен по цене", last_price, "так как ниже нижней границы канала")
        enter = last_price
        for i in channel_id:
            bot.send_message(chat_id=i, text=f"Position enter{interval}\n{enter}\n LONG")
        PROFIT_FLAG = True

    #else:
    #
    #   say_text(f'Ничего не делаем. Последняя цена",{last_price}, "находится в границах канала')
    #  print("Ничего не делаем. Последняя цена", last_price, "находится в границах канала")
    return profit, PROFIT_FLAG, FLAG, enter

def main():
    FLAG = [None, None, None, None,]
    PROFIT_FLAG = [None, None, None, None,]
    total_profit = 0
    ol_profit = 0
    enter = [0, 0, 0, 0]

    while True:
        try:
            profit_t1 = channel_enter(client, '1m',PROFIT_FLAG[0],FLAG[0], enter[0])
            profit_t15 = channel_enter(client, '15m', PROFIT_FLAG[1], FLAG[1], enter[1])
            profit_t1h = channel_enter(client, '1h', PROFIT_FLAG[2], FLAG[2], enter[2])
            profit_t4h = channel_enter(client, '4h', PROFIT_FLAG[3], FLAG[3], enter[3])
            total_profit += profit_t1[0] + profit_t15[0] + profit_t1h[0] + profit_t4h[0]
            PROFIT_FLAG[0] = profit_t1[1]
            PROFIT_FLAG[1] = profit_t15[1]
            PROFIT_FLAG[2] = profit_t1h[1]
            PROFIT_FLAG[3] = profit_t4h[1]
            FLAG[0] = profit_t1[2]
            FLAG[1] = profit_t15[2]
            FLAG[2] = profit_t1h[2]
            FLAG[3] = profit_t4h[2]
            enter[0] = profit_t1[3]
            enter[1] = profit_t15[3]
            enter[2] = profit_t1h[3]
            enter[3] = profit_t4h[3]
            if ol_profit != total_profit:
                    ol_profit = total_profit
                    #print(f"Points Total profit\n{ol_profit}")
                    for i in channel_id:
                        bot.send_message(chat_id=i, text=f"Points Total profit\n{ol_profit}")
        except:
            print('Error')

        time.sleep(5)


if __name__ == '__main__':
    main()
