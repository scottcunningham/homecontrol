#!/usr/bin/env python3

from flask import Blueprint, request
from flask import render_template
import configparser
import requests
import subprocess
import json
from subprocess import PIPE

CMD = "sudo amixer -q -c 2 sset PCM 5%{}"
SET_CMD = "sudo amixer -q -c 2 sset PCM {}%"
UP_CMD = CMD.format('+')
DOWN_CMD = CMD.format('-')
# -c = card --- open alsamixer, F6, pick card number
# get $x --- $x should be the bottom of the bar in alsamixer, eg Speaker, PCM, etc
GET_CMD = ['sudo', "sh", "-c",
           "amixer -c 2 get PCM | awk '/Front Left:/ { print $5 \"|\" $7 }'"]
MUTE_CMD = 'sudo amixer -c 2 sset PCM toggle'
REFRESH_PLAYLIST_CMD = 'sudo service mopidy restart'

MOPIDY_HOST = 'http://localhost/mopidy/rpc'
MOPIDY_CONFIG_FILE = '/etc/mopidy/mopidy.conf'

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
    vol, muted = get_vol()
    print('vol is', vol, ' muted:', muted)
    if muted:
        return "{}% [muted]".format(vol)
    return "{}%".format(vol)


@vol_blueprint.route('/mute')
def mute():
    run_cmd(MUTE_CMD)
    return 'mute!'


@vol_blueprint.route('/')
def main():
    return render_template('vol.html')


@vol_blueprint.route('/refresh')
def refresh():
    restart_mopidy()
    return 'refreshing playlists (restarting mopidy lol)'


def restart_mopidy():
    run_cmd(REFRESH_PLAYLIST_CMD)


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


@vol_blueprint.route('/setuser/<user>')
def switch_user(user):
    set_spotify_user(user)
    restart_mopidy()
    return "switched to user {}".format(user)


@vol_blueprint.route('/getuser/')
def get_user():
    return current_spotify_user()


def run_mopidy_cmd(method):
    data = {"jsonrpc": "2.0", "id": 1, "method": method}
    resp = requests.post(MOPIDY_HOST, data=json.dumps(data))
    if resp.status_code/100 != 2:
        raise Exception('Mopidy API call {} failed with status {}, error {}'
                        .format(method, resp.status_code, resp.content))
    return json.loads(resp.content.decode('utf-8'))


def run_cmd(cmd, shell=False):
    return subprocess.check_call(cmd.split(), shell=shell)


def get_vol():
    stdout = subprocess.Popen(GET_CMD, stdout=PIPE).communicate()[0]
    vol, muted = stdout.decode('utf-8').replace('[', '').replace(']', '').replace('%', '').split('|')
    muted = "off" in muted
    print(stdout, "==>", vol, muted)
    return vol, muted


def current_spotify_user():
    with open(MOPIDY_CONFIG_FILE) as cf:
        config = configparser.ConfigParser()
        config.readfp(cf)
        return config.get('spotify', 'username')


def get_user_spotify_config(user):
        with open(MOPIDY_CONFIG_FILE) as cf:
            config = configparser.ConfigParser()
            config.readfp(cf)
        section = 'spotify_{}'.format(user)
        return {x: config.get(section, x) for x in
            ['username', 'password', 'client_id', 'client_secret']}


def set_spotify_user(new_user):
    new_config = get_user_spotify_config(new_user)
    with open(MOPIDY_CONFIG_FILE, 'r') as cf:
        config = configparser.ConfigParser()
        config.readfp(cf)
        for field in ['username', 'password', 'client_id', 'client_secret']:
            config.set('spotify', field, new_config[field])

    with open(MOPIDY_CONFIG_FILE, 'w') as cf:
        config.write(cf)
