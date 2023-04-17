import configparser
import json

from telethon.sync import TelegramClient
from telethon import connection
from config import *
# для корректного переноса времени сообщений в json
from datetime import date, datetime
from telethon.tl.functions.users import GetFullUserRequest
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest







async def dump_all_participants(channel):
	"""Записывает json-файл с информацией о всех участниках канала/чата"""
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 100   # максимальное число записей, передаваемых за один раз

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
	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	limit_msg = 100   # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = 50000 # поменяйте это значение, если вам нужны не все сообщения

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
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	with open('channel_messages.json', 'w', encoding='utf8') as outfile:
		 json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

async def find_user(user_id):

    full = await client(GetFullUserRequest(user_id)) # Получаем ник из id
    user_name = full.users[0].username
    print(user_name)
    with open("users.txt", "a") as file:
        file.writelines(f'@{user_name}\n')


async def main(chanal_name, client):
	client = client


	channel = await client.get_entity(chanal_name)
	#await dump_all_participants(channel)
	await dump_all_messages(channel)

	with open('channel_messages.json', 'r', encoding='utf8') as outfile:
		user = json.load(outfile)  # загнали все, что получилось в переменную

	user_list = []
	for i in user:
		if i['from_id']['user_id'] in user_list:
			print(i['from_id']['user_id'], 'error')
		else:
			user_list.append(i['from_id']['user_id'])
	for i in user_list:
		with client:
			try:
				client.loop.run_until_complete(find_user(i), client)
			except:
				print('error')

client = TelegramClient(PHONE, API_ID, API_HASH)

client.connect()
for chanel in CHANNEL_PARS:
	with client:
		client.loop.run_until_complete(main(chanel, client))