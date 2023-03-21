import json
# data = [{
#     'user_id':'',
#     'position_1m':'',
#     'position_5m':'',
#     'position_15m':'',
#     'position_30m':'',
#     'position_1h':'',
#     'position_4h':'',
#
# }]
# with open('data2.txt', 'w') as outfile:
#
#     json.dump(data, outfile)
def set_user_js(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        user =[]
        for i in data:
            print(i)
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

def del_user_js(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                data.pop(data.index(i))
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


def get_position_js(user_id, position ):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            if str(user_id) == i['user_id']:
                return i[position]

def get_all_position(user_id):
    with open('data2.txt') as json_file:
        data = json.load(json_file)
        for i in data:
            minim=10000000
            maxim=0
            position = 0
            if str(user_id) == i['user_id']:
                for pos in i:
                    if pos == 'user_id':
                        pass
                    elif i[pos] == '':
                        pass
                    else:
                        if i[pos][0] > maxim:
                            maxim = i[pos][0]
                        elif i[pos][0] < minim:
                            minim = i[pos][0]
                        position += i[pos][1]
                return   position,  minim, maxim


# set_user_js(4555)
#del_user_js(4555)
# print(get_position_js(4555,'position_15m'))
# print(get_position_js(4555,'position_5m'))
# print(get_position_js(4555,'position_1m'))
# print(get_position_js(4555,'position_1h'))
# set_position_js(4555,'position_15m', 20000)
print(get_all_position(871610428))