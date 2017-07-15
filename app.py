#!/usr/bin/env python

from flask import Flask

from vol import vol_blueprint
from fan import fan_blueprint
from gui import gui_blueprint


if __name__ == '__main__':
    app = Flask(__name__)
    app.register_blueprint(vol_blueprint, url_prefix='/vol')
    app.register_blueprint(fan_blueprint, url_prefix='/fan')
    app.register_blueprint(gui_blueprint, url_prefix='/homecontrol')
    app.run(port=1337, debug=True)
