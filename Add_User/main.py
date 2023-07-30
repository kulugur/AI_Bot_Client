import configparser
import json
import pandas
from telethon.sync import TelegramClient
from telethon import connection
from config import *
# для корректного переноса времени сообщений в json
from datetime import date, datetime
from telethon.tl.functions.users import GetFullUserRequest
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest, JoinChannelRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest







async def dump_all_participants(channel):
	print('start dump_all_participants')
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 1000  # максимальное число записей, передаваемых за один раз

	all_participants = []   # список всех участников канала
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel,
			filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	all_users_details = []   # список словарей с интересующими параметрами участников канала

	for participant in all_participants:
		all_users_details.append({"id": participant.id,
			"first_name": participant.first_name,
			"last_name": participant.last_name,
			"user": participant.username,
			"phone": participant.phone,
			"is_bot": participant.bot})

	with open('channel_users.json', 'w', encoding='utf8') as outfile:
		json.dump(all_users_details, outfile, ensure_ascii=False)


async def dump_all_messages(channel):
	print('start dump_all__messages')
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 1000   # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 50000# поменяйте это значение, если вам нужны не все сообщения

	class DateTimeEncoder(json.JSONEncoder):
		'''Класс для сериализации записи дат в JSON'''
		def default(self, o):
			if isinstance(o, datetime):
				return o.isoformat()
			if isinstance(o, bytes):
				return list(o)
			return json.JSONEncoder.default(self, o)

	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages
		for message in messages:
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		print('сообшения', total_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

async def find_user(user_id):
	print('start find_user')
	with open("all_users.txt", "r") as file:
		users = file.readlines()



	full = await client(GetFullUserRequest(user_id)) # Получаем ник из id
	user_name = full.users[0].username


	with open("all_users.txt", "a") as file:

		if f'@{user_name}\n' in users:
			pass
		else:
			file.writelines(f'@{user_name}\n')



async def get_my_user(my_client):
	print('start get_my_user')
	client = TelegramClient(my_client[0], my_client[1], my_client[2])
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

	ds = pandas.DataFrame()
	ds['user_id'] = user_id
	ds['username'] = username_list
	ds['first_name'] = first_name_list
	ds['last_name'] = last_name_list
	ds['phone'] = phone_list
	ds.to_csv('my_subscribers.csv', index=False)

async def comparison_users():
	print('start comparison_users')
	with open("my_users.txt", "w") as file:
		emp_ds = pandas.read_csv('my_subscribers.csv')
		user_name = emp_ds.username
		for user in user_name:
			if user == user:
				file.write(f'@{user}\n')

	with open("users.txt", "w") as file:
		print("users.txt создан")
	with open("all_users.txt", "r") as file:
 		users = file.readlines()
	print(users)
	with open("my_users.txt", "r") as file:
		my_users = file.readlines()
	for i in users:
		if i in my_users:
			pass
		else:
			with open("users.txt", "a") as file:
				file.write(i)



async def main(chanel):
	print('srart main')
	channel = await client.get_entity(chanel)
	# await dump_all_participants(channel)
	await dump_all_messages(channel)

	with open('channel_messages.json', 'r', encoding='utf8') as outfile:
		user = json.load(outfile)  # загнали все, что получилось в переменную

	user_list = []
	for i in user:
		try:
			if i['from_id']['user_id'] in user_list:
				print(i['from_id']['user_id'], 'error')
			else:
				user_list.append(i['from_id']['user_id'])
		except:
			print('нет ID')
	for i in user_list:
		async with client:
			try:
				await find_user(i)
			except:
				print('error')
	await get_my_user(my_client)
	await comparison_users()






client = TelegramClient(my_client[0], my_client[1], my_client[2])
client.connect()

with client:
	client.loop.run_until_complete(main(CHANNEL_PARS))

