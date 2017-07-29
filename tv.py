from flask import Blueprint, render_template
from pylgtv import WebOsClient
from collections import OrderedDict

import sys
import logging
import json


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

tv_blueprint = Blueprint('tv', __name__)


inputs = OrderedDict(json.load(open('conf/tv_inputs.json')))
apps = OrderedDict(json.load(open('conf/tv_apps.json')))


@tv_blueprint.route('/open/<app>')
def open_app(app):
    print ("Opening app", app)
    try:
        webos_client = WebOsClient('192.168.1.162')
        webos_client.launch_app(apps[app]['uri'])
        return "Opening {}".format(app)
    except Exception as e:
        print("Error connecting to TV")
        print(str(e))
        return "Failed to open {}: {}".format(app, str(e))


@tv_blueprint.route('/')
def list_apps():
    return render_template('tv.html', apps=apps, inputs=inputs)
