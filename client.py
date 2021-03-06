import requests
from config import ip
from config import port

protocol = "http://"


br_before_off = 50

def get_lamps_list():
    l_list = requests.get(protocol + ip + ":" + str(port) + "/api/lamps")
    return l_list.json()


def update_lamp(_id, name, power, brightness, group=''):
    # print(name, brightness)
    req = requests.put(protocol + ip + ":" + str(port) + "/api/lamp/" + str(_id),
                       json={'id': _id, 'name': name, 'group': group, 'power': power, 'brightness': brightness})
    return req.status_code


def brightness_up(name, n):
    for i in get_lamps_list():
        if i['name'] == name:
            if i['brightness'] + n >= 100:
                update_lamp(i['id'], i['name'], i['power'], 100)
                return 100
            else:
                update_lamp(i['id'], i['name'], i['power'], i['brightness'] + n)
                return i['brightness'] + n


def brightness_down(name, n):
    for i in get_lamps_list():
        if i['name'] == name:
            if i['brightness'] - n <= 0:
                update_lamp(i['id'], i['name'], i['power'], 0)
                return 0
            else:
                update_lamp(i['id'], i['name'], i['power'], i['brightness'] - n, )
                return i['brightness'] - n


def turn(name):
    global br_before_off
    for i in get_lamps_list():
        if i['name'] == name:
            if i['brightness']:
                br_before_off = i['brightness']
                update_lamp(i['id'], i['name'],  i['power'], 0)
            else:
                update_lamp(i['id'], i['name'], i['power'], br_before_off)


def is_power(name):
    for i in get_lamps_list():
        if i['name'] == name:
            if i['brightness'] != 0:
                return True
    return False
