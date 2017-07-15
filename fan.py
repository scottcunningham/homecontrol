#!/usr/bin/env python

from flask import Blueprint
from pyHS100 import SmartPlug

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
