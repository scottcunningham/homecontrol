#!/usr/bin/env python

import json
from flask import Blueprint
from pyHS100 import SmartPlug
from flask import render_template

fan_blueprint = Blueprint('fan', __name__)


@fan_blueprint.route('/toggle')
def fantoggle():
    p = SmartPlug('192.168.1.188')
    # print('On?', p.is_on)
    if p.is_on:
        p.turn_off()
        return 'turned fan off'
    else:
        p.turn_on()
        return 'turned fan on'


@fan_blueprint.route('/status')
def fan_status():
    p = SmartPlug('192.168.1.188')
    return json.dumps({'fan': p.is_on})


@fan_blueprint.route('/')
def view():
    return render_template('fans.html')
