#!/usr/bin/env python

from flask import Blueprint, request
from flask import render_template
import requests
import subprocess
import json
from subprocess import PIPE

CMD = "amixer -q -c 1 sset PCM 5%{}"
SET_CMD = "amixer -q -c 1 sset PCM {}%"
UP_CMD = CMD.format('+')
DOWN_CMD = CMD.format('-')
GET_CMD = ["sh", "-c",
           "amixer -c 1 get PCM | awk '/Front Left:/ { print $5 }'"]
MUTE_CMD = 'amixer -c 1 sset PCM toggle'
REFRESH_PLAYLIST_CMD = 'sudo service mopidy restart'

MOPIDY_HOST = 'http://localhost/mopidy/rpc'

vol_blueprint = Blueprint('vol', __name__)


@vol_blueprint.route('/up')
def up():
    run_cmd(UP_CMD)
    return 'up!'


@vol_blueprint.route('/down')
def down():
    run_cmd(DOWN_CMD)
    return 'down!'


@vol_blueprint.route('/set')
def set():
    percent = request.args.get('percent')
    run_cmd(SET_CMD.format(percent))
    return 'set to {}!'.format(percent)


@vol_blueprint.route('/get')
def get():
    vol = get_vol()
    print 'vol is', vol
    return vol


@vol_blueprint.route('/mute')
def mute():
    run_cmd(MUTE_CMD)
    return 'mute!'


@vol_blueprint.route('/')
def main():
    return render_template('index.html')


@vol_blueprint.route('/refresh')
def refresh():
    run_cmd(REFRESH_PLAYLIST_CMD)
    return 'refreshing playlists (restarting mopidy lol)'


@vol_blueprint.route('/fantoggle')
def fantoggle():
    return 'use /fan/toggle now'


@vol_blueprint.route('/playpause')
def playpause():
    status = run_mopidy_cmd('core.playback.get_state')['result']
    if status == 'playing':
        run_mopidy_cmd(method='core.playback.pause')
        return json.dumps({'status': 'paused'})
    else:
        run_mopidy_cmd(method='core.playback.play')
        return json.dumps({'status': 'playing'})


@vol_blueprint.route('/track/next')
def next_track():
    run_mopidy_cmd('core.playback.next')
    return 'next'


@vol_blueprint.route('/track/prev')
def prev_track():
    run_mopidy_cmd('core.playback.previous')
    return 'prev'


def run_mopidy_cmd(method):
    data = {"jsonrpc": "2.0", "id": 1, "method": method}
    resp = requests.post(MOPIDY_HOST, data=json.dumps(data))
    if resp.status_code/100 != 2:
        raise Exception('Mopidy API call {} failed with status {}, error {}'
                        .format(method, resp.status_code, resp.content))
    return json.loads(resp.content)


def run_cmd(cmd, shell=False):
    print cmd
    return subprocess.check_call(cmd.split(), shell=shell)


def get_vol():
    stdout = subprocess.Popen(GET_CMD, stdout=PIPE).communicate()[0]
    return stdout
