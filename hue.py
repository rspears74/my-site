import requests
import json

USERNAME = "TA2JPwy5BjQfzJ102l-kN8gXbJOC3M6O9OH80XjM"

IP_ADDR = "192.168.0.100"

BASEURL = "http://" + IP_ADDR + "/api/" + USERNAME + "/"
nice_yellow = {'hue': 14974, 'sat': 140}
nice_white = {'hue': 32980, 'sat': 50}


def get_all_lights():
    return json.loads(requests.get(BASEURL + 'lights/').text)


# lights is a lights object from the get_all_lights() method
# on_off is bool
# color is a dict that contains 'hue' and 'sat' values
def set_all_lights_state(lights, on_off, color):
    for light in lights:
        requests.put(BASEURL + 'lights/' + light + '/state',
                data=json.dumps({'on': on_off,
                                'hue': color['hue'],
                                'bri': 254,
                                'sat': color['sat']}))


def turn_lights_on_off(data):
    lights = data['lights']
    on_off = data['on_off']
    for light in lights:
        requests.put(BASEURL + 'lights/' + light + '/state',
                data=json.dumps({'on': on_off}))


def get_all_groups():
    return json.loads(requests.get(BASEURL + 'groups/').text)

def set_group_state(group_num, on_off, color):
    requests.put(BASEURL + 'groups/' + str(group_num) + '/action',
                data=json.dumps({'on': on_off,
                                'hue': color['hue'],
                                'bri': 254,
                                'sat': color['sat']}))
