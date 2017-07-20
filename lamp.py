#!/usr/bin/env python

import json
from flask import Blueprint
from pyHS100 import SmartPlug

lamp_blueprint = Blueprint('lamp', __name__)


@lamp_blueprint.route('/toggle')
def lamptoggle():
    p = SmartPlug('192.168.1.190')
    # print('On?', p.is_on)
    if p.is_on:
        p.turn_off()
        return 'turned lamp off'
    else:
        p.turn_on()
        return 'turned lamp on'


@lamp_blueprint.route('/status')
def lamp_status():
    p = SmartPlug('192.168.1.190')
    return json.dumps({'status': p.is_on})
