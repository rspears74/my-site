from flask import Blueprint, jsonify, request, session, redirect, url_for,\
flash
from flask_restful import Resource, Api
import requests
import json
from functools import wraps
from extensions import login_required

USERNAME = "TA2JPwy5BjQfzJ102l-kN8gXbJOC3M6O9OH80XjM"
IP_ADDR = "192.168.0.100"
BASEURL = "http://" + IP_ADDR + "/api/" + USERNAME + "/"


hue = Api(Blueprint('hue', __name__))


def get_all_lights():
    return json.loads(requests.get(BASEURL + 'lights/').text)


def turn_lights_on_off(data):
    lights = data['lights']
    on_off = data['on_off']
    for light in lights:
        requests.put(BASEURL + 'lights/' + light + '/state',
                data=json.dumps({'on': on_off}))


@hue.resource('/check-all-lights')
class CheckLights(Resource):
    @login_required
    def get(self):
        return jsonify(get_all_lights())


@hue.resource('/set-lights')
class SetLights(Resource):
    @login_required
    def put(self):
        data = request.get_json(force=True)
        return jsonify(turn_lights_on_off(data))
