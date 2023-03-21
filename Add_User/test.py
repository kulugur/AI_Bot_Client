#import pandas as pd
import json

with open('channel_users.json', 'r', encoding='utf8') as outfile:
    user = json.load(outfile)  # загнали все, что получилось в переменную
    print(user)  # вывели результат на экран