from config import *
from telethon import TelegramClient
import pandas as pd
import asyncio

async def main():
    client = TelegramClient(PHONE, API_ID, API_HASH)

    client = await client.start()
    dialogs = await client.get_dialogs()

    channels = {d.entity.username: d.entity
                for d in dialogs
                if d.is_channel}
    print(channels)


    my_channel = MY_CHANNEL.split('/')[-1]
    channel_my = channels[my_channel]

    members_telethon_list_my = await client.get_participants(channel_my, aggressive=True)




    user_id = [member.id for member in members_telethon_list_my]
    username_list = [member.username for member in members_telethon_list_my]
    first_name_list = [member.first_name for member in members_telethon_list_my]
    last_name_list = [member.last_name for member in members_telethon_list_my]
    phone_list = [member.phone for member in members_telethon_list_my]

    ds = pd.DataFrame()
    ds['user_id'] = user_id
    ds['username'] = username_list
    ds['first_name'] = first_name_list
    ds['last_name'] = last_name_list
    ds['phone'] = phone_list
    ds.to_csv('my_subscribers.csv', index=False)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())