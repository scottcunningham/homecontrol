#!/usr/bin/env python3.6

import json
from flask import Blueprint, jsonify, render_template, abort, Response
from pyHS100 import SmartPlug

plugs_blueprint = Blueprint('plugs', __name__)

plugs = json.load(open('conf/plugs.json'))


@plugs_blueprint.route('/')
def view():
    return render_template('plugs.html', plugs=plugs)


@plugs_blueprint.route('/list')
def list():
    return jsonify(plugs)


@plugs_blueprint.route('/toggle/<plug>')
def plug_toggle(plug):
    print("Toggling plug", plug)
    ip = plugs[plug]['ip']
    try:
        p = SmartPlug(ip)
    except Exception as e:
        return abort(Response(
            'Failed to query smart plug at {}, error {}'.format(ip, str(e))
        ))

    if p.is_on:
        p.turn_off()
        new_state = False
    else:
        p.turn_on()
        new_state = True

    return jsonify({
        'status': new_state,
        'action': 'toggled',
    })


@plugs_blueprint.route('/status/<plug>')
def plug_status(plug):
    p = SmartPlug(plugs[plug]['ip'])
    return jsonify({'status': p.is_on})
