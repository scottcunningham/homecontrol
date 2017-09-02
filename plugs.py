#!/usr/bin/env python3

import json
from flask import Blueprint
from flask import render_template
from pyHS100 import SmartPlug

plugs_blueprint = Blueprint('plugs', __name__)

plugs = json.load(open('conf/plugs.json'))

@plugs_blueprint.route('/')
def view():
    return render_template('plugs.html', plugs=plugs)


@plugs_blueprint.route('/toggle/<plug>')
def plug_toggle(plug):
    print("Toggling plug", plug)
    p = SmartPlug(plugs[plug]['ip'])
    if p.is_on:
        p.turn_off()
        return 'turned {} off'.format(plug)
    else:
        p.turn_on()
        return 'turned {} on'.format(plug)


@plugs_blueprint.route('/status/<plug>')
def plug_status(plug):
    p = SmartPlug(plugs[plug]['ip'])
    return json.dumps({'status': p.is_on})
